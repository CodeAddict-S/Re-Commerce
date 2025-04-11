from django.contrib import admin
from products.models import (
    DiscountEvent,
    ProductReview,
    CategoryGroup,
    Product,
    Category,
    ProductImage
)
from django.contrib.admin.exceptions import AlreadyRegistered

models = [DiscountEvent, ProductReview, CategoryGroup, Category, Product, ProductImage]

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass

# Register your models here.