from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Game
from .models import LFGPost, Event, ROLE_CHOICES, RANK_CHOICES
from .forms import LFGPostForm, EventForm


def lfg_list(request):
    posts = LFGPost.objects.filter(is_active=True).select_related('author', 'game')
    game_id = request.GET.get('game')
    role = request.GET.get('role')
    rank = request.GET.get('rank')
    games = Game.objects.all()

    if game_id:
        posts = posts.filter(game_id=game_id)
    if role:
        posts = posts.filter(role=role)
    if rank:
        posts = posts.filter(rank=rank)

    return render(request, 'lfg/list.html', {
        'posts': posts,
        'games': games,
        'roles': ROLE_CHOICES,
        'ranks': RANK_CHOICES,
        'selected_game': game_id,
        'selected_role': role,
        'selected_rank': rank,
    })


def lfg_detail(request, pk):
    post = get_object_or_404(LFGPost.objects.select_related('author', 'game'), pk=pk)
    return render(request, 'lfg/detail.html', {'post': post})


@login_required
def lfg_create(request):
    if request.method == 'POST':
        form = LFGPostForm(request.POST)
        if form.is_valid():
            lfg = form.save(commit=False)
            lfg.author = request.user
            lfg.save()
            messages.success(request, 'Оголошення опубліковано!')
            return redirect('lfg:detail', pk=lfg.pk)
    else:
        form = LFGPostForm()
    return render(request, 'lfg/form.html', {'form': form, 'title': 'Нове оголошення'})


@login_required
def lfg_edit(request, pk):
    post = get_object_or_404(LFGPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Ви не можете редагувати чуже оголошення.')
        return redirect('lfg:detail', pk=pk)
    if request.method == 'POST':
        form = LFGPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оголошення оновлено.')
            return redirect('lfg:detail', pk=pk)
    else:
        form = LFGPostForm(instance=post)
    return render(request, 'lfg/form.html', {'form': form, 'title': 'Редагувати оголошення', 'post': post})


@login_required
def lfg_delete(request, pk):
    post = get_object_or_404(LFGPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Ви не можете видалити чуже оголошення.')
        return redirect('lfg:detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Оголошення видалено.')
        return redirect('lfg:list')
    return render(request, 'lfg/confirm_delete.html', {'object': post, 'type': 'LFG оголошення'})


def event_list(request):
    events = Event.objects.select_related('author', 'game').prefetch_related('participants')
    game_id = request.GET.get('game')
    games = Game.objects.all()
    if game_id:
        events = events.filter(game_id=game_id)
    return render(request, 'lfg/event_list.html', {
        'events': events,
        'games': games,
        'selected_game': game_id,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event.objects.select_related('author', 'game').prefetch_related('participants'), pk=pk)
    is_participant = request.user.is_authenticated and event.participants.filter(pk=request.user.pk).exists()
    return render(request, 'lfg/event_detail.html', {
        'event': event,
        'is_participant': is_participant,
    })


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            event.participants.add(request.user)
            messages.success(request, 'Подію створено!')
            return redirect('lfg:event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'lfg/event_form.html', {'form': form, 'title': 'Нова подія'})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.author != request.user:
        messages.error(request, 'Ви не можете редагувати чужу подію.')
        return redirect('lfg:event_detail', pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подію оновлено.')
            return redirect('lfg:event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'lfg/event_form.html', {'form': form, 'title': 'Редагувати подію', 'event': event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.author != request.user:
        messages.error(request, 'Ви не можете видалити чужу подію.')
        return redirect('lfg:event_detail', pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Подію видалено.')
        return redirect('lfg:event_list')
    return render(request, 'lfg/confirm_delete.html', {'object': event, 'type': 'подію'})


@login_required
def event_join(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.is_full:
        messages.warning(request, 'Подія вже заповнена.')
    elif event.participants.filter(pk=request.user.pk).exists():
        messages.info(request, 'Ви вже зареєстровані на цю подію.')
    else:
        event.participants.add(request.user)
        messages.success(request, 'Ви приєдналися до події!')
    return redirect('lfg:event_detail', pk=pk)


@login_required
def event_leave(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.author == request.user:
        messages.warning(request, 'Організатор не може покинути власну подію.')
    else:
        event.participants.remove(request.user)
        messages.success(request, 'Ви покинули подію.')
    return redirect('lfg:event_detail', pk=pk)
