from django.db import models
from django.contrib.auth import get_user_model
from .education import Education
from posts.models import Post
User = get_user_model()


class Profile(models.Model):
    contact_number = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        default='default.jpg', upload_to='profile_pics')
    address = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.ForeignKey(
        Education, related_name='profile_education', on_delete=models.PROTECT)
    post = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.user.username
