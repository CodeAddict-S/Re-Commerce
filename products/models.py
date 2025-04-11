from django.db import models
from utils.models import BaseModel
from imagekit.models import ImageSpecField
from django.utils.text import slugify
from users.models import User
import uuid

# Create your models here.
class CategoryGroup(BaseModel):
    name = models.CharField(max_length=255)

class Category(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=10000, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    category_group = models.ForeignKey(CategoryGroup, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        if Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        self.slug = slug
        super().save(*args, **kwargs)

class Product(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(max_length=10000, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    thumbnail = models.ImageField()
    resized_thumbnail = ImageSpecField(source='thumbnail', format='JPEG', options={'quality': 7})
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        if Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        self.slug = slug
        super().save(*args, **kwargs)

class ProductImage(BaseModel):
    image = models.ImageField()
    resized_image = ImageSpecField(source='image', format='JPEG', options={'quality':15})
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

class ProductReview(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=10000)
    stars = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField()

    def save(self, *args, **kwargs):
        if self.stars < 0 or self.stars > 5:
            raise ValueError('ProductReview.stars must be between 0 and 5')
        super().save(*args, **kwargs)

class DiscountEvent(BaseModel):
    products = models.ManyToManyField(Product)
    discount = models.IntegerField()
    slogan = models.CharField(max_length=255)
    banner = models.ImageField(null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.discount < 0 or self.discount > 100:
            raise ValueError('Discount is Invalid')
        super().save(*args, **kwargs)
