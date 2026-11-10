from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from users.models import Game
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.select_related('author', 'game').prefetch_related('comments')
    game_id = request.GET.get('game')
    search = request.GET.get('q', '').strip()
    games = Game.objects.all()

    if game_id:
        posts = posts.filter(game_id=game_id)
    if search:
        posts = posts.filter(title__icontains=search) | posts.filter(content__icontains=search)

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'posts/list.html', {
        'posts': posts,
        'games': games,
        'selected_game': game_id,
        'search': search,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author', 'game'), pk=pk)
    comments = post.comments.select_related('author').all()
    form = CommentForm()
    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост опубліковано!')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/form.html', {'form': form, 'title': 'Новий пост'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Ви не можете редагувати чужий пост.')
        return redirect('posts:detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост оновлено.')
            return redirect('posts:detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/form.html', {'form': form, 'title': 'Редагувати пост', 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Ви не можете видалити чужий пост.')
        return redirect('posts:detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост видалено.')
        return redirect('posts:list')
    return render(request, 'posts/confirm_delete.html', {'object': post, 'type': 'пост'})


@login_required
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('posts:detail', pk=pk)


@login_required
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post_id=post_pk)
    if comment.author != request.user:
        messages.error(request, 'Ви не можете видалити чужий коментар.')
    elif request.method == 'POST':
        comment.delete()
        messages.success(request, 'Коментар видалено.')
    return redirect('posts:detail', pk=post_pk)
