from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

from blog import views
from blog.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # sitemap generator
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    url(r'^', include('blog.urls',
                      namespace='blog',
                      app_name='blog')),

    url(r'^contact/',
        views.contact,
        name='contact'),

    url(r'^about/',
        views.about_page,
        name='about'),

    url(r'^ckeditor/',
        include('ckeditor_uploader.urls')),
]

# DEVELOPMENT ONLY
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)