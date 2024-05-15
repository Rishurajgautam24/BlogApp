from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Blog
from .form import BlogForm
from django.http import HttpResponseForbidden
from django.urls import reverse

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        auth_logout(request)
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnfpassword = request.POST.get('confirm-password')
        if password == cnfpassword:
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('login')
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
    return render(request, 'signup.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def blog_detail(request, slug):
    blog_obj = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog_obj': blog_obj})

def see_blog(request):
    blog_objs = Blog.objects.all()
    return render(request, 'see_blog.html', {'blog_objs': blog_objs})

def add_blog(request, slug=None):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if slug:
        blog_obj = get_object_or_404(Blog, slug=slug)
        if blog_obj.user != request.user:
            return HttpResponseForbidden("You don't have permission to edit this blog post.")
        form = BlogForm(request.POST or None, request.FILES or None, instance=blog_obj)
    else:
        form = BlogForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        blog = form.save(commit=False)
        blog.user = request.user
        blog.save()
        return redirect('see_blog')

    return render(request, 'add_blog.html', {'form': form})

def edit_blog(request, slug):
    blog_obj = get_object_or_404(Blog, slug=slug)
    if not request.user.is_authenticated or blog_obj.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this blog post.")
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog_obj)
        if form.is_valid():
            form.save()
            return redirect('see_blog')
    else:
        form = BlogForm(instance=blog_obj)

    return render(request, 'edit_blog.html', {'form': form, 'blog_obj': blog_obj})

def delete_blog(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    
    blog_obj = get_object_or_404(Blog, slug=slug)
    if blog_obj.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this blog post.")
    
    blog_obj.delete()
    return redirect('see_blog')
