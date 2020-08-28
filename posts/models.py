from django.db import models
from django.contrib.auth import get_user_model
from accounts.models.education import Education
USER = get_user_model()


class Post(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    post_slug = models.SlugField(unique=True)
    caption = models.TextField()
    education = models.ForeignKey(
        Education, on_delete=models.PROTECT)
    file = models.FileField(upload_to='posts/files/', blank=True, null=True)
    stars_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-posted_at', )

    def __str__(self):
        return self.caption[:20] + '...'


class Comment(models.Model):
    commented_at = models.DateTimeField(auto_now_add=True)
    comment_modified_at = models.DateTimeField(auto_now=True)
    comment_description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    stars_count = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_description[:20] + '...'

    class Meta:
        ordering = ('-commented_at', )
