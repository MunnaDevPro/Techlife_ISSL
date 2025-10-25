from django.db import models
from django.utils import timezone
from blog_post.models import BlogPost
from accounts.models import CustomUserModel


class EarningSetting(models.Model):
    view_rate = models.FloatField(default=0.01)      
    like_rate = models.FloatField(default=0.50)     
    comment_rate = models.FloatField(default=1.00)  
    quality_rate = models.FloatField(default=1.00)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return f"Earning Rates (Updated: {self.updated_at.date()})"


# class ContentQuality(models.Model):
#     post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name="quality_score")
#     content_score = models.FloatField(default=1.0)  # future a manually add korbo or ai use korbo
#     evaluated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.post.title} - Quality: {self.content_score}"
    

