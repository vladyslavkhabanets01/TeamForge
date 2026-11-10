from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField('Назва', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Гра'
        verbose_name_plural = 'Ігри'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField('Про себе', blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    discord = models.CharField('Discord', max_length=100, blank=True)
    steam = models.CharField('Steam', max_length=100, blank=True)
    games = models.ManyToManyField(Game, verbose_name='Ігри', blank=True)

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

    def __str__(self):
        return f'Профіль {self.user.username}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('users:profile', kwargs={'username': self.user.username})
