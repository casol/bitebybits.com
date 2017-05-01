from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .forms import ContactForm


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


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        # Form was submitted
        # Crated a form instance using submitted data
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            # Message body with name and email
            message = 'You have a message from {} ({}):\n\n{}'.format(form.cleaned_data['name'],
                                                                      form.cleaned_data['email'],
                                                                      form.cleaned_data['message'])
            try:
                send_mail(subject, message, from_email, ['contactfrombitstobytes@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect(reverse('success'))
    return render(request, 'blog/contact.html', {'form': form})


def success(request):
    return render(request, 'blog/success.html',)
