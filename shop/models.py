from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Return a hierarchical category name (e.g., 'Parent / Child')."""
        return f"{self.parent.name + ' / ' if self.parent else ''}{self.name}"

    def get_all_products(self):
        """Return products in this category and its direct subcategories."""
        subcategories = list(self.subcategories.all())
        return Product.objects.filter(category__in=[self] + subcategories)


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='subcategories_of_category',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
