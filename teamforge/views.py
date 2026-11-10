from django.shortcuts import render
from posts.models import Post
from lfg.models import LFGPost, Event


def home(request):
    recent_posts = Post.objects.select_related('author', 'game').all()[:6]
    recent_lfg = LFGPost.objects.filter(is_active=True).select_related('author', 'game').all()[:4]
    upcoming_events = Event.objects.select_related('author', 'game').prefetch_related('participants').all()[:3]
    return render(request, 'home.html', {
        'recent_posts': recent_posts,
        'recent_lfg': recent_lfg,
        'upcoming_events': upcoming_events,
    })
