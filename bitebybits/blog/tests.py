from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
# from django.core.urlresolvers import reverse  # Deprecated since version 1.10
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage
from django.utils.cache import force_text

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

    def test_view_uses_correct_template(self):
        response = self.c.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        # Check if requested template is used
        self.assertTemplateUsed(response, 'blog/post/list.html')

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


class PaginationTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        number_of_posts = 10
        # Crate a list of objects for pagination
        for post_num in range(number_of_posts):
            Post.objects.create(title='Test this', slug='test-this', body='Test', author=self.user,
                                created=timezone.now(),
                                status='published')

    def test_number_of_posts_created(self):
        self.assertEqual(Post.objects.count(), 10)

    def test_paginator(self):
        paginator = Paginator(Post.objects.all(), 5)
        self.assertEqual(10, paginator.count)
        self.assertEqual(2, paginator.num_pages)
        self.assertEqual([1, 2], list(paginator.page_range))

    def test_invalid_page(self):
        paginator = Paginator(Post.objects.all(), 5)
        self.assertRaises(InvalidPage, paginator.page, 7)

    #def test_first_page_instead_of_invalide(self):
       # paginator = Paginator(Post.objects.all(), 5)
       # p = paginator.page(7)
        #self.assertEqual('<Page 1 of 2>', force_text(p))
       # self.assertEqual(EmptyPage, p, 1)


class PostTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.p = Post.objects.create(title='Test this', slug='test-this', body='Test', author=self.user,
                                     created=timezone.now(),
                                     status='published')

    def test_post_creation(self):
        """test_post_creation() should return title for post field title"""
        self.assertTrue(isinstance(self.p, Post))
        self.assertEqual(self.p.__str__(), self.p.title)

    def test_post_title_field(self):
        field_title = self.p._meta.get_field('title').verbose_name
        self.assertEqual(field_title, 'title')

    def test_post_title_field_max_length(self):
        max_length = self.p._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_post_slug_field(self):
        field_slug = self.p._meta.get_field('slug').verbose_name
        self.assertEqual(field_slug, 'slug')

    def test_post_slug_field_max_length(self):
        max_length = self.p._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_post_body_field(self):
        field_body = self.p._meta.get_field('body').verbose_name
        self.assertEqual(field_body, 'body')

    def test_get_absolute_url(self):
        self.assertEqual(self.p.get_absolute_url(), '/blog/2017/05/17/test-this/')

    def test_post_fields(self):
        """test_post_fields() should return all post model fields."""
        # Create the post
        post = Post()
        post.title = 'Test post, post test'
        post.body = 'You have to test'
        post.slug = 'test-post-post-test'
        post.created = timezone.now()
        # Create user
        post.author = self.user
        # Save it
        post.save()
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 2)
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


