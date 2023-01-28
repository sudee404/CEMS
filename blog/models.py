from django.db import models
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from creator.models import UserProfile
# Create your models here.



class Post(models.Model):
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=200,help_text='Enter Post title',unique=True)
    image = models.ImageField(upload_to='images',default='default.png',help_text='Pictures relating to post')
    content = HTMLField()
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    create_date = models.DateField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True,null=True)
    featured = models.BooleanField(default=False)
    

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    """This model holds the blog post categories
    """
    name = models.CharField(max_length=200,unique=True)
    image = models.ImageField(upload_to='image',default='image/default.png')
    
    @property
    def post_count(self):
        return Post.objects.filter(category=self)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
       self.image.name = f"{self.name}.{self.image.name.split('.')[-1]}"
       super().save(*args, **kwargs)

import uuid
class PostInstance(models.Model):
    """model representing particular instance of a post that is to be starred"""
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="unique id for this specific post")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    starrer = models.ForeignKey('auth.User',on_delete=models.SET_NULL,null=True)
    starred = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['post','starrer']    
        
    def star(self,request):
        self.starred = True
        self.starrer = request.user
        self.save()
    
    def __str__(self):
        return self.post.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    author_name = models.CharField(max_length=200,default='Anonymous')
    author = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    text = HTMLField()
    created_at = models.DateTimeField(default=timezone.now)
        
    def get_absolute_url(self):
        return reverse("post-list")
    
    def __str__(self):
        return f'{self.author_name} '

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete = models.CASCADE)
    author = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    text = HTMLField()
    created_at = models.DateTimeField(default=timezone.now)


    