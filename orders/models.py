from django.db import models
from utils.models import BaseModel
from users.models import User
from products.models import Product

# Create your models here.
class Order(BaseModel):
    status_options = {
        "pending": "pending",
        "delivering": "delivering",
        "received": "received",
        "cancelled": "cancelled",
        "asking_for_refund": "asking_for_refund",
        "refund_accepted": "refund_accepted"
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyers_orders')
    status = models.CharField(max_length=255, choices=status_options)

class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')

