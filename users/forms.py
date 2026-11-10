from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Нікнейм'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Підтвердження пароля'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'discord', 'steam', 'games']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'discord': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username#0000'}),
            'steam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Steam нікнейм'}),
            'games': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'bio': 'Про себе',
            'avatar': 'Аватар',
            'discord': 'Discord',
            'steam': 'Steam',
            'games': 'Улюблені ігри',
        }
