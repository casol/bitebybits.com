from django.test import TestCase, Client
from django.utils import timezone
# from django.core.urlresolvers import reverse  # Deprecated since version 1.10
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.core.mail import send_mail, BadHeaderError
from django.core.files.uploadedfile import SimpleUploadedFile


from blog.models import Post, PostImage
from blog.forms import ContactForm
from blog import sitemaps, feeds


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
        self.assertEqual(self.p.get_absolute_url(), '/blog/2017/05/20/test-this/')

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


class TestAdminPanel(TestCase):
    def create_user(self):
        self.username = 'test_admin'
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user

    def test_spider_admin(self):
        self.create_user()
        client = Client()
        client.login(username=self.username, password=self.password)
        admin_pages = [
            '/admin/',
            '/admin/blog/post/',
            '/admin/blog/post/add/',
            '/admin/sites/site/',
            '/admin/taggit/tag/',
            '/admin/auth/',
            '/admin/auth/group/',
            '/admin/auth/group/add/',
            '/admin/auth/user/',
            '/admin/auth/user/add/',
            '/admin/password_change/'
        ]
        for page in admin_pages:
            resp = client.get(page)
            assert resp.status_code == 200


class ContactFormTest(TestCase):
    """Testing contact form."""
    """
    def test_renew_form_date_field_label(self):
        form = ContactForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'name')
    """
    def test_header(self):
        """test_header should return true if BadHeaderError occur."""
        error_occured = False
        try:
            send_mail('Header\nInjection', 'Here is the message.', 'from@example.com',
                      ['to@example.com'], fail_silently=False)
        except BadHeaderError:
            error_occured = True
        self.assertTrue(error_occured)


class PostDetailTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.post = Post.objects.create(title='Test this', slug='test-this', body='Test',
                                        author=self.user, created=timezone.now(), status='published')
        i = SimpleUploadedFile(name='foo.gif',
                               content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\''
                                       b'x01\x00\x00\x02\x02D\x01\x00')
        self.post_image = PostImage.objects.create(post=self.post, image=i,
                                                   image_title='test0', image_author='someone')

        self.url = self.post.get_absolute_url()

    def test_post_with_status_published(self):
        """A published post should by visible"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post, response.context['post'])
        self.assertNumQueries(1)

    def test_post_with_status_unpublished(self):
        """Post with status draft or trashed should not be visible test
        should return 404."""
        self.post.status = 'draft'
        self.post.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TestEntrySitemap(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.post_1 = Post.objects.create(title='Test this1', slug='test-this1', body='Test1',
                                          author=self.user, created=timezone.now(), status='published')
        self.post_2 = Post.objects.create(title='Test this2', slug='test-this2', body='Test2',
                                          author=self.user, created=timezone.now(), status='published')
        self.post_3 = Post.objects.create(title='Test this3', slug='test-this3', body='Test3',
                                          author=self.user, created=timezone.now(), status='published')
        self.post_4 = Post.objects.create(title='Test this4', slug='test-this4', body='Test4',
                                          author=self.user, created=timezone.now(), status='draft')
        self.entry_map = sitemaps.PostSitemap()

    def test_items(self):
        """test_items() should only return published entries."""
        actual_entries = self.entry_map.items()

        expected_slugs = ['test-this3', 'test-this2', 'test-this1']
        actual_slugs = [post.slug for post in actual_entries]

        self.assertEqual(actual_slugs, expected_slugs)
        self.assertNumQueries(1)

    def test_last_modified(self):
        """test_last_modified() should be able to get the last update from a post"""
        actual_update = self.entry_map.lastmod(self.post_3)

        now = timezone.now()
        self.assertGreaterEqual(now, actual_update)
        self.assertGreaterEqual(actual_update, self.post_1.publish)


class TestLatestPostsFeed(TestCase):
    """Test blog feeds."""

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.post_1 = Post.objects.create(title='Test this1', slug='test-this1', body='Test1',
                                          author=self.user, created=timezone.now(), status='published')
        self.post_2 = Post.objects.create(title='Test this2', slug='test-this2', body='Test2',
                                          author=self.user, created=timezone.now(), status='published')
        self.post_3 = Post.objects.create(title='Test this3', slug='test-this3', body='Test3',
                                          author=self.user, created=timezone.now(), status='published')
        self.post_4 = Post.objects.create(title='Test this4', slug='test-this4', body='Test4',
                                          author=self.user, created=timezone.now(), status='draft')

        self.feed = feeds.LatestPostFeed()

    def test_feed_properties(self):
        actual_entries = self.feed.items()

        expected_slugs = ['test-this3', 'test-this2', 'test-this1']
        actual_slugs = [post.slug for post in actual_entries]
        response = self.c.get('/blog/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual_slugs, expected_slugs)
        self.assertNumQueries(1)


