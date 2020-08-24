from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User  = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=300)
    meta_description = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    STATUS_CHOICES = (('Published', 'published'), ('Draft', 'draft'))
    status = models.CharField(max_length=10, default='Draft',
                              choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='images/')
    tags = models.ManyToManyField(Tag)
    stars_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_image_url(self, obj):
        return obj.image.url


