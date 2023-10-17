
from django.contrib import admin
from django.urls import path,include
from froala_editor import views as editor_views
from .views import *



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="see_blog""),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path('froala_editor/',include('froala_editor.urls')),
    path('blog-detail/<slug>', blog_detail, name="blog_detail"),
    path("see_blog/", see_blog, name="see_blog"),
    path('add-blog/', add_blog, name="add_blog"),
    path('edit-blog/<slug>', edit_blog, name="edit_blog"),
    path('delete-blog/<slug>', delete_blog, name="delete_blog"),

]
