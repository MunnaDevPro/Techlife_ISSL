from django.db import models
from accounts.models import CustomUserModel


class Question(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='questions',default=1)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='answers',default=1)
    content = models.TextField()
    image = models.ImageField(upload_to='answers_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return f"Answer by {self.author} on '{self.question.title}'"

