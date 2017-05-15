from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User

from blog.models import Post


class PostTest(TestCase):
    def test_create_post(self):
        # Create the post
        post = Post()
        post.title = 'Test post, post test'
        post.body = 'You have to test'
        post.slug = 'test-post-post-test'
        post.created = timezone.now()
        # Create user
        u = User(1)
        u.save()
        post.author = u
        # Save it
        post.save()
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Check attributes
        self.assertEquals(only_post.title, 'Test post, post test')
        self.assertEquals(only_post.body, 'You have to test')
        self.assertEquals(only_post.slug, 'test-post-post-test')
        self.assertEquals(only_post.created.day, post.created.day)
        self.assertEquals(only_post.created.month, post.created.month)
        self.assertEquals(only_post.created.year, post.created.year)
        self.assertEquals(only_post.created.hour, post.created.hour)
        self.assertEquals(only_post.created.minute, post.created.minute)
        self.assertEquals(only_post.created.second, post.created.second)


class AdminTest(LiveServerTestCase):
    def test_login(self):
        # Create client
        c = Client()

        response = c.get('/admin/', fallow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Log in' in response.content)


class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)


