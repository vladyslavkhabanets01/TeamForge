from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'game']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва поста'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Текст поста...'}),
            'game': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Зміст',
            'game': 'Гра (необов\'язково)',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Написати коментар...',
            }),
        }
        labels = {'content': ''}
