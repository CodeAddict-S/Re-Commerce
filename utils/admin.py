from django.contrib import admin
from products.models import (
    Product,
    ProductImage,
    Category
)

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)