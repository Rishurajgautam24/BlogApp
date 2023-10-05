from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import *
from .form import *
from django.shortcuts import get_object_or_404
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
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:
                return redirect('login')

    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        auth_logout(request)
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cnfpassword = request.POST.get('confirm-password')
            # print(username,email, password,cnfpassword)
            if password == cnfpassword:
                print("Password Matched")
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('login')

    return render(request, 'signup.html')

def logout(request):
    auth_logout(request)
    return redirect("/login")


def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = Blog.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)


def see_blog(request):
    context = {}
    try:
        blog_objs = Blog.objects.all()
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context)

# def add_blog(request):
#     if request.user.is_authenticated:
#         context = {'form': BlogForm}
#         try:
#             if request.method == 'POST':
#                 form = BlogForm(request.POST)
#                 print(request.FILES)
#                 image = request.FILES.get('image', '')
#                 title = request.POST.get('title')
#                 print(title)
#                 user = request.user if request.user.is_authenticated else None

#                 if form.is_valid():
#                     print('Valid')
#                     content = form.cleaned_data['content']

#                 blog_obj = Blog.objects.create(
#                     user=user, title=title,
#                     content=content, image=image
#                 )
#                 print(blog_obj)
#                 return redirect('/add-blog/')
#         except Exception as e:
#             print(e)

#         return render(request, 'add_blog.html', context)
#     else:
#         return redirect('login')
def add_blog(request, slug=None):
    if request.user.is_authenticated:
        context = {}
        if slug:
            blog_obj = Blog.objects.get(slug=slug)
            if blog_obj.user == request.user:
                form = BlogForm(request.POST or None, request.FILES or None, instance=blog_obj)
                context['form'] = form
                if form.is_valid():
                    form.save()
                    return redirect('/see_blog/')  # Redirect to the blog detail page after editing
            else:
                return HttpResponseForbidden("You don't have permission to edit this blog post.")
        else:
            form = BlogForm(request.POST or None, request.FILES or None)
            context['form'] = form
            if form.is_valid():
                new_blog = form.save(commit=False)
                new_blog.user = request.user
                new_blog.save()
                return redirect('/see_blog/')  # Redirect to the blog detail page after creating a new blog

        return render(request, 'add_blog.html', context)
    else:
        return redirect('login')


# def edit_blog(request, slug):
#     model=Blog
#     template_name = 'edit_blog.html'
#     fields = ['title', 'content', 'image']
#     success_url = '/see_blog/' 

#     # update blog with new details on the page
#     if request.user.is_authenticated:
#         try:
#             blog_obj = Blog.objects.filter(slug=slug).first()
#             form = BlogForm(request.POST or None, instance=blog_obj)
#             if form.is_valid():
#                 form.save()
#                 return redirect('/see_blog/')
#             return render(request, template_name, {'form': form})
#         except Exception as e:
#             print(e)
#         return redirect('/see_blog/')
#     else:
#         return redirect('login')
def edit_blog(request, slug):
    blog_obj = get_object_or_404(Blog, slug=slug)
    template_name = 'edit_blog.html'
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog_obj)
        if form.is_valid():
            form.save()
            success_url = reverse('see_blog')
            return redirect(success_url)
    else:
        form = BlogForm(instance=blog_obj)

    return render(request, template_name, {'form': form})

    
    

    

    
    


def delete_blog(request, slug):
    if request.user.is_authenticated:
        try:
            blog_obj = Blog.objects.filter(slug=slug).first()
            blog_obj.delete()
            return redirect('/see_blog/')
        except Exception as e:
            print(e)
        return redirect('/see_blog/')
    else:
        return redirect('login')
    
