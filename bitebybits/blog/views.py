from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Post


def post_list(request):
    """
    Displaying list of all posts with status published.
    """
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    """
    Post detail view takes year, month, day and slug parameters
    to retrieve a published post with requested slug and date.
    """
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def about_page(request):
    return render(request, 'blog/about.html',)
