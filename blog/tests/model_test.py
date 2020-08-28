from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Blog, Category, Comment, Subscriber
from django.urls import reverse


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a user
        testuser1 = get_user_model().objects.create_user(
            username='testuser1',
            email='test@gmail.com',
            password='123456789'
        )
        testuser1.save()
        # create a blog
        programming = Category.objects.create(name='Python')
        test_post = Blog.objects.create(
            user=testuser1,
            title ='New Blog title',
            subtitle ='simple title',
            category = programming,
            meta_description =' a web app blog testing haha',
            content ='Content will goes here.',
        )
        test_post.save()

    def test_blog_content(self):
        post = Blog.objects.get(id=1)
        title = f'{post.title}'
        category = f'{post.category}'
        subtitle = f'{post.subtitle}'
        meta_description = f'{post.meta_description}'
        content = f'{post.content}'

        #   self.assertEqual(user,'testuser1','testuser1')
        self.assertEqual(title, 'New Blog title')
        self.assertEqual(subtitle, 'simple title')
        self.assertEqual(meta_description, ' a web app blog testing haha')
        self.assertEqual(content, 'Content will goes here.')

class SubscriberTests(TestCase):

   def setUp(self):
       test_subscriber = Subscriber.objects.create(
           name='ram',
           email="hello@gmail.com"
       )

   def test_email_content(self):
       subscriber = Subscriber.objects.get(id=1)
       expected_object_name = f'{subscriber.email}'
       self.assertEquals(expected_object_name, 'hello@gmail.com')
        
class CommentTests(TestCase):
    def setUp(self):
        test_comment = Comment.objects.create(
                name = 'lol',
                email = 'lol@gmail.com',
                message = 'shai ho',
        )

    def test_comment(self):
        comment = Comment.objects.get(id=1)
        name = f'{comment.name}'
        email = f'{comment.email}'
        message = f'{comment.message}'

        self.assertEqual(name,'lol'),
        self.assertEqual(email,'lol@gmail.com')
        self.assertEqual(message,'shai ho')
