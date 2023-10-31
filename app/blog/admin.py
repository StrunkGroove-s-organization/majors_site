# blog/admin.py

from django.contrib import admin
from .models import Post, PostImage, ImageCaption  # Добавляем модель ImageCaption

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1  # Количество пустых форм для добавления изображений

class ImageCaptionInline(admin.TabularInline):  # Добавляем встроенный интерфейс для подписей
    model = ImageCaption
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    inlines = [ImageCaptionInline]  # Встроенный интерфейс для редактирования подписей

# Теперь регистрируем модели ImageCaption
admin.site.register(ImageCaption)
