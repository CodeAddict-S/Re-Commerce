from django.db import models

# Create your models here.
class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='%(class)s_created_by')
    created_at = models.DateTimeField()
    updated_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='%(class)s_updated_by')
    updated_at = models.DateTimeField()

    class Meta:
        abstract = True