from django.db import models
from blog_post.models import BlogPost
from accounts.models import CustomUserModel
class Favorite(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # akta user double favorite dite parbena 1 ta post er jonno


    def __str__(self):
        return f"{self.user.email} favorited {self.post.title}"


class Share(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="shares")
    user = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, blank=True)

    platform = models.CharField(max_length=50, choices=[
        ("facebook", "Facebook"),
        ("twitter", "Twitter / X"),
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
        ("others", "Others"),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} shared on {self.platform}"
