from django.contrib import admin
from .models import Category, Post, PostInstance,Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','publish_date')

class PostInline(admin.TabularInline):
    '''Tabular Inline View for Post'''

    model = Post

    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','created_at')


admin.site.register(PostInstance)
admin.site.register(Category)