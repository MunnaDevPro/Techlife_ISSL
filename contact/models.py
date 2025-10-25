from django.db import models
from accounts.models import CustomUserModel
class contact_or_support(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="contact_user", null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
