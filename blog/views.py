from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Post, Contact, Comment
from .forms import ContactForm, CommentForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import SignInForm
from django.contrib.auth.decorators import login_required

def index(request):
    p = Post.objects.order_by('-created_at')
    return render(request, 'index.html', {'posts': p})

def about(request):
    return render(request, 'about.html')

def post(request, pk):
    p = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post)
    post_is_liked = p.likes.filter(id=request.user.id).exists()
    post_is_disliked = p.dislikes.filter(id=request.user.id).exists()
    
    context = {
        'posts': p,
        'comments': comments,
        'post_is_liked': post_is_liked,
        'post_is_disliked': post_is_disliked,
        'like_count': p.likes.count(),
        'dislike_count': p.dislikes.count(),
    }
    return render(request, 'post.html', {'posts': p, 'comments': comments, "context": context})

def comment_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        comments = Comment.objects.create(post=post, name=request.user.username, text=text)
        return redirect('post', pk=post_id)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            user = Contact(name=name, email=email, phone=phone, message=message)
            user.save()
            subject = f"Regarding {message}"
            message = f'{message} {phone}'
            send_mail(subject, message, email, ['randomstring890@gmail.com'], fail_silently=False)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('/contact/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# def BlogPostLike(request, pk):
#     post_instance = get_object_or_404(Post, id=pk)
#     action = request.POST.get('action')
    
#     if action == 'like':
#         if post_instance.likes.filter(id=request.user.id).exists():
#             post_instance.likes.remove(request.user)
#         else:
#             post_instance.likes.add(request.user)
#     elif action == 'dislike':
#         if post_instance.dislikes.filter(id=request.user.id).exists():
#             post_instance.dislikes.remove(request.user)
#         else:
#             post_instance.dislikes.add(request.user)
    
#     post_is_liked = post_instance.likes.filter(id=request.user.id).exists()
#     post_is_disliked = post_instance.dislikes.filter(id=request.user.id).exists()
    
#     return post(request, pk)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login_user/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
