from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
class Post(models.Model):
    title = models.CharField(max_length=200)
    sub_title=models.CharField(max_length=100)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes =models.ManyToManyField(User,related_name="blogpost_like")
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    def number_of_likes(self):
        return self.likes.count()


    class Meta:
        ordering=['created_at']

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return a string that includes the commenter's name and a snippet of the comment text
        # return f'{self.name} - {self.text[:50]}'
        return self.text




class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.IntegerField()
    message=models.TextField()
    sent_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['sent_at']
    
    def __str__(self):
        return self.name
