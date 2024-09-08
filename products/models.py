from django.db import models
from categories.models import SubCategory


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    has_variants = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def category(self):
        return self.subcategory.category

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.has_variants and not self.variants.exists():

            ProductVariant.objects.get_or_create(
                product=self,
                sku=f"{self.id}-default",
                defaults={'price': self.price, 'stock': self.stock}
            )


class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.id}"


class ProductVariantAttribute(models.Model):
    variant = models.ForeignKey(ProductVariant, related_name='variant_attributes', on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variant.sku} - {self.attribute_value}"
