from django.db import models

# Create your models here.

class Message(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ], default='MEDIUM')
    
    # News specific fields
    source_name = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
