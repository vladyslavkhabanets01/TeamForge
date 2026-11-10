from django.db import models
from django.contrib.auth.models import User
from users.models import Game

ROLE_CHOICES = [
    ('any', 'Будь-яка'),
    ('support', 'Підтримка'),
    ('tank', 'Танк'),
    ('dps', 'DPS'),
    ('healer', 'Хілер'),
    ('carry', 'Керрі'),
    ('jungler', 'Джанглер'),
]

RANK_CHOICES = [
    ('any', 'Будь-який'),
    ('bronze', 'Бронза'),
    ('silver', 'Срібло'),
    ('gold', 'Золото'),
    ('platinum', 'Платина'),
    ('diamond', 'Діамант'),
    ('master', 'Майстер'),
    ('grandmaster', 'Грандмайстер'),
]


class LFGPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lfg_posts', verbose_name='Автор')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Гра', related_name='lfg_posts')
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='any')
    rank = models.CharField('Ранг', max_length=20, choices=RANK_CHOICES, default='any')
    description = models.TextField('Опис')
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        verbose_name = 'LFG оголошення'
        verbose_name_plural = 'LFG оголошення'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} шукає команду в {self.game.name}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('lfg:detail', kwargs={'pk': self.pk})


class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', verbose_name='Організатор')
    title = models.CharField('Назва', max_length=200)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Гра', related_name='events')
    description = models.TextField('Опис')
    event_date = models.DateTimeField('Дата проведення')
    max_players = models.PositiveIntegerField('Максимум гравців', default=10)
    participants = models.ManyToManyField(User, related_name='joined_events', verbose_name='Учасники', blank=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        verbose_name = 'Подія'
        verbose_name_plural = 'Події'
        ordering = ['event_date']

    def __str__(self):
        return self.title

    @property
    def participants_count(self):
        return self.participants.count()

    @property
    def is_full(self):
        return self.participants.count() >= self.max_players

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('lfg:event_detail', kwargs={'pk': self.pk})
