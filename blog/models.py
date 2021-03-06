from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """
    Custom manager for retrieving all post with
    status 'published'.
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='published')


class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('trashed', 'Trashed')
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=250, default='')
    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               related_name='blog_posts')
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICE,
                              default='draft')

    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager

    # taggit
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    """
    Model responsible for storing images.
    """
    post = models.ForeignKey(Post)
    image = models.ImageField(upload_to='images/')
    image_title = models.CharField(max_length=200)
    image_author = models.CharField(max_length=150)
    image_description = models.CharField(max_length=250, blank=True)
    image_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_title


