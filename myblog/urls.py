
from django.contrib import admin
from django.urls import path
from blog.views import index,about,contact,post,comment_detail,login_user,register_user,logout_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('post/<int:pk>/',post,name='post'),
    path('post/<int:post_id>/comment/',comment_detail,name='comment'),
    # path('post/<int:pk>/like/', BlogPostLike, name='blogpost_like'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),



]
