from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    preview_text = models.TextField(blank=True, null=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    preview_image = models.ImageField(
        upload_to='blog_images/', blank=True, null=True
    )

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return f"Image for {self.post.title}"

class ImageCaption(models.Model):
    post_image = models.ForeignKey(
        PostImage, on_delete=models.CASCADE, related_name='captions'
    )
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.caption
