from django.contrib import admin
from .models import *


blog_models = [
    blog.Category,
    blog.Tag,
    blog.Blog,
]

comment_models = [
    comment.Comment,
    subscriber.Subscriber,
]

admin.site.register(blog_models)
admin.site.register(comment_models)