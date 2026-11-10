# TeamForge

[🇺🇦 Українська](README.md) &nbsp;|&nbsp; 🇬🇧 English

A social platform for gamers — find your team, share experience, organize events.

## Features

- **Gamer profiles** — avatar, favorite games, Discord, Steam
- **Posts & comments** — publications with filtering by game and keyword search
- **Teammate search (LFG)** — filter by game, role and rank
- **Game events** — create, join/leave, participant counter
- **Authentication** — register, login, logout, protection of other users' records

## Tech Stack

- Python 3.14 / Django 6.1
- Bootstrap 5.3 (dark theme)
- SQLite
- Pillow (avatar uploads)

## Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate

# 3. Load initial data (games)
python manage.py loaddata fixtures/games.json

# 4. Create a superuser
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Site: http://127.0.0.1:8000  
Admin panel: http://127.0.0.1:8000/admin

## Optional: load sample data

```bash
python manage.py create_sample_data
```

Creates 5 demo users (password: `pass1234`), 8 posts, 24 comments, 6 LFG listings and 5 events.

## Project Structure

```
teamforge/      — project settings & main URLs
users/          — profiles, authentication, Game model
posts/          — posts and comments
lfg/            — LFG listings and events
templates/      — HTML templates (Bootstrap 5 dark theme)
fixtures/       — initial data (10 games)
```

## Database

SQLite with 9 tables connected via Django ORM:

| Table | Description |
|---|---|
| `auth_user` | Built-in Django users (hashed passwords) |
| `users_game` | Game catalog |
| `users_userprofile` | Extended gamer profiles |
| `posts_post` | Publications |
| `posts_comment` | Comments on posts |
| `lfg_lfgpost` | Looking-for-group listings |
| `lfg_event` | Game events with participant tracking |
