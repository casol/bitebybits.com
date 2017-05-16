from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
# from django.core.urlresolvers import reverse  # Deprecated since version 1.10
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post


class PostListTest(TestCase):
    """Testing post list front page."""
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_post_list_access(self):
        """Get a page which shows all blog post at url/blog/."""
        response = self.c.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_custom_managers(self):
        """Testing custom manager methods. Create two entries one with status published
         and another with status draft."""
        Post.objects.create(title='Test', body='Test', author=self.user, status='published')
        Post.objects.create(title='Test', body='Test', author=self.user, status='draft')
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.published.count(), 1)

    def test_post_list_template_context(self):
        """Only published entries should be shown on list post page."""
        # create few blog entries
        Post.objects.create(title='Test', slug='test', body='Test', author=self.user,
                            status='draft',
                            created=timezone.now())
        Post.objects.create(title='Test', slug='test', body='Test', author=self.user,
                            status='draft',
                            created=timezone.now())
        Post.objects.create(title='Test', slug='test', body='Test', author=self.user,
                            created=timezone.now(),
                            status='published')

        response = self.c.get(reverse('blog:post_list'))
        # assert that context contains only published entries
        self.assertEqual(len(response.context['posts']), 1)


    #def test_

class PostTest(TestCase):
    def test_create_post(self):
        # Create the post
        post = Post()
        post.title = 'Test post, post test'
        post.body = 'You have to test'
        post.slug = 'test-post-post-test'
        post.created = timezone.now()

        # Create user
        user = User.objects.create_user(username="test", email="test@test.com", password="test")
        post.author = user
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
        self.assertEqual(response.status_code, 302)
        #self.assertTrue('Log in' in response.content)


class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)


