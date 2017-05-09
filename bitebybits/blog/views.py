from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings

from .models import Post, PostImage
from .forms import ContactForm

# Google reCAPTCHA
import urllib
import json

from taggit.models import Tag


def post_list(request, tag_slug=None):
    """
    Displaying list of all posts with status published or
    posts tagged with a specific tag.
    """
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        # Retrieving Tag object with the given slug
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Filtering the list of posts with given tag
        object_list = object_list.filter(tags__in=[tag])

    #  Paginator a list of objects, plus the number of items to show on each page
    paginator = Paginator(object_list, 3)  # Show 3 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        #  # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'page': page,
                   'tag': tag})


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
    #images = PostImage.get(post
    #images = get_object_or_404(PostImage)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
                   #'images': images})


def about_page(request):
    return render(request, 'blog/about.html',)


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        # Form was submitted
        # Crated a form instance using submitted data
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            # Begin reCAPTCHA validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # End reCAPTCHA validation

            if result['success']:
                # reCAPTCHA passed validation
                name = form.cleaned_data['name']
                from_email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                # Message body with name and email
                message = 'You have a message from {} ({}):\n\n{}'.format(form.cleaned_data['name'],
                                                                          form.cleaned_data['email'],
                                                                          form.cleaned_data['message'])
                try:
                    send_mail(subject,
                              message,
                              from_email,
                              ['contactfrombitstobytes@gmail.com'],
                              fail_silently=False)
                    messages.success(request, 'Thank you! Your email was sent and '
                                              'I will get back to you as soon as I can.')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            else:
                messages.error(request, 'Oh snap! Better check yourself, change '
                                        'a few things up and try submitting again.')
    return render(request, 'blog/contact.html', {'form': form})
