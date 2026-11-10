from django import forms
from .models import LFGPost, Event


class LFGPostForm(forms.ModelForm):
    class Meta:
        model = LFGPost
        fields = ['game', 'role', 'rank', 'description', 'is_active']
        widgets = {
            'game': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'rank': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': 'Розкажіть про себе: стиль гри, коли граєте, що очікуєте від команди...',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'game': 'Гра',
            'role': 'Роль',
            'rank': 'Ранг',
            'description': 'Опис',
            'is_active': 'Активний пошук',
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'game', 'description', 'event_date', 'max_players']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва події'}),
            'game': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'event_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'max_players': forms.NumberInput(attrs={'class': 'form-control', 'min': 2, 'max': 100}),
        }
        labels = {
            'title': 'Назва',
            'game': 'Гра',
            'description': 'Опис',
            'event_date': 'Дата та час',
            'max_players': 'Максимум гравців',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.event_date:
            self.initial['event_date'] = self.instance.event_date.strftime('%Y-%m-%dT%H:%M')
