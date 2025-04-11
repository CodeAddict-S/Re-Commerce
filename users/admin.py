from django.contrib import admin
from users.models import (
    User,
    Merchant,
    MerchantApplication
)

# Register your models here.
admin.site.register(User)
admin.site.register(Merchant)
admin.site.register(MerchantApplication)