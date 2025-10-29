from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from blog_post.models import BlogPost  

from accounts.models import CustomUserModel
class SavedPost(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="saved_posts")
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="saved_posts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # same user cannot save same post multiple times

    def __str__(self):
        return f"{self.user} saved {self.post.title}"
