from django.db import models
from . blog import Blog
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    name = models.CharField(max_length=120)
    author = models.ForeignKey(User, null=True, related_name="comments", on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    message = models.TextField()
    stars_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    @property
    def data(self):
        return{
            "pk": self.pk,
            "comment": self.message,
            "author": self.author.username if self.author else "",
            "name": self.name,
            "email": self.email,
        }


class Reaction(models.Model):
    comment = models.OneToOneField(Comment,on_delete = models.CASCADE)
    likes = models.PositiveIntegerField(default = 0)
    dislikes = models.PositiveIntegerField(default = 0 )


    def _increase_count(self, field):
        self.refresh_from_db()
        setattr(self, field, models.F(field) + 1)
        self.save(update_fields=[field])

    def _decrease_count(self, field):
        self.refresh_from_db()
        setattr(self, field, models.F(field) - 1)
        self.save(update_fields=[field])
