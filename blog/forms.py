from django import forms
from .models import Post, Comment, Reply
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content','image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'content':TinyMCE(attrs={'class':'bg-dark'})
        }
        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'author')

        labels = {
            'text':'Comment',
            'author':'Name'
        }
