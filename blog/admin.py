from django.contrib import admin
from .models import Post,Contact,Comment
@admin.register(Post)

class BlogPost(admin.ModelAdmin):
    list_display=['id','title','content','author','created_at','updated_at']


@admin.register(Contact)

class BlogPost(admin.ModelAdmin):
    list_display=['id','name','email','phone','message','sent_at']


@admin.register(Comment)

class BlogPost(admin.ModelAdmin):
    list_display=['id','name','text','post','post_date']