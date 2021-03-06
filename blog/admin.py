from django.contrib import admin

from .models import Post, PostImage


class InlineImage(admin.StackedInline):
    """
    Allows to upload image on the same page as a parent model"
    """
    model = PostImage
    # Controls the number of extra forms fields
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author',
                    'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    # automatically generate the value for slug
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    inlines = [InlineImage]

admin.site.register(Post, PostAdmin)

