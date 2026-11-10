from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from users.models import Game, UserProfile
from posts.models import Post, Comment
from lfg.models import LFGPost, Event


USERS = [
    {'username': 'shadowhunter',  'email': 'shadow@tf.com',   'bio': 'Граю вже 7 років. Люблю тактичні ігри та стратегії. Шукаю серйозну команду для рейтингових матчів.', 'discord': 'shadowhunter#1337', 'steam': 'shadowhunter_gg', 'games': [1, 2, 4]},
    {'username': 'neonviper',     'email': 'neon@tf.com',     'bio': 'Support main в Dota 2. Завжди готовий допомогти команді. Граю кожен день після роботи.', 'discord': 'neonviper#4200', 'steam': 'neon_viper', 'games': [1, 5, 8]},
    {'username': 'frostbyte',     'email': 'frost@tf.com',    'bio': 'Колишній напівпрофесійний гравець у CS. Зараз граю для задоволення, але хочу повернутись у рейтинг.', 'discord': 'frostbyte#9999', 'steam': 'frostbyte_pro', 'games': [2, 3, 6]},
    {'username': 'galaxystorm',   'email': 'galaxy@tf.com',   'bio': 'Casual gamer, граю у вільний час. Люблю Minecraft та Fortnite. Завжди в гарному настрої!', 'discord': 'galaxystorm#0001', 'steam': 'galaxystorm', 'games': [9, 10, 7]},
    {'username': 'ironclad',      'email': 'iron@tf.com',     'bio': 'Tank main, граю у MMO та MOBA. WoW рейдер з 10-річним досвідом. Шукаю гільдію для хардкор рейдингу.', 'discord': 'ironclad#5555', 'steam': 'ironclad_wow', 'games': [8, 1, 3]},
]

POSTS = [
    {'author': 'shadowhunter', 'game': 2, 'title': 'Топ-5 порад для початківців у CS2', 'content': 'Привіт всім! Сьогодні хочу поділитися порадами, які допоможуть вам швидше прогресувати в CS2.\n\n1. Завжди слухайте кроки — звук у цій грі вирішує все\n2. Вчіться кидати гранати — правильний flash може виграти раунд\n3. Не стріляйте на ходу — зупиніться перед пострілом\n4. Вивчіть одну карту ідеально, а не всі поверхнево\n5. Дивіться демо своїх програних матчів — там найбільше навчального матеріалу\n\nПишіть у коментарях свої поради!'},
    {'author': 'neonviper',   'game': 1, 'title': 'Чому Support — найважливіша роль у Dota 2', 'content': 'Багато гравців недооцінюють роль саппорта. Але саме від нього залежить 60% перемог команди.\n\nЯк хороший саппорт ти:\n- Контролюєш руни та нейтралів\n- Забезпечуєш вижити кері на лейні\n- Ставиш вардів у ключових місцях\n- Ініціюєш або контролюєш ініціацію\n\nОстаннє оновлення дуже підсилило Heroes підтримки. Зараз це мета і вам варто спробувати!'},
    {'author': 'frostbyte',   'game': 3, 'title': 'League of Legends — огляд патчу 14.10', 'content': 'Новий патч приніс серйозні зміни до балансу чемпіонів.\n\nУсилено:\n- Jinx: +5% до базового AD\n- Thresh: покращена механіка хука\n- Yasuo: зменшено кулдаун вітру\n\nОслаблено:\n- Briar: зменшено базове HP на 50\n- K\'Sante: нерф до Q damage\n\nЗагалом патч збалансований. Jungle мета залишається домінуючою. Чекаємо ваших думок!'},
    {'author': 'galaxystorm', 'game': 9, 'title': 'Побудував замок у Minecraft — ділюся скіншотами', 'content': 'Нарешті завершив свій мегапроект — середньовічний замок з підземеллям, мостами та навіть діючою фермою редстоуну!\n\nЩо використав:\n- Deepslate та Blackstone для стін\n- Copper для даху з патиною\n- Sculk sensors для автоматичних дверей\n\nБудував 3 тижні по 2 години щодня. Якщо хочете — можу поділитися seed та координатами. Пишіть у коментарях!'},
    {'author': 'ironclad',    'game': 8, 'title': 'Гайд по рейдингу у WoW: як підготуватися до Mythic', 'content': 'Mythic рейдинг — це вершина PvE контенту у World of Warcraft. Ось що вам потрібно:\n\nОбов\'язково:\n- Item level мінімум 480+\n- Знання всіх механік бою напам\'ять\n- Вікод логів через Warcraft Logs\n- Discord з push-to-talk\n\nБажано:\n- Weakauras для відстеження дебафів\n- DBMA або BigWigs для рейд попереджень\n- Мінімум 3 місяці досвіду у Normal/Heroic\n\nЯкщо є питання — питайте!'},
    {'author': 'shadowhunter', 'game': 4, 'title': 'Valorant: новий агент Clove — мій досвід', 'content': 'Погрував з тиждень на новому агенті Clove і готовий поділитися враженнями.\n\nСильні сторони:\n- Унікальна пасивна здатність після смерті\n- Гарний контроль диму\n- Висока виживаність\n\nСлабкі сторони:\n- Складний у вивченні\n- Залежний від мікрофону у команді\n- Не підходить для соло-рейтингу\n\nЗагалом цікавий агент для досвідчених гравців. 7/10'},
    {'author': 'neonviper',   'game': 5, 'title': 'Overwatch 2: повертаємося до 6v6?', 'content': 'Blizzard анонсували тестування повернення формату 6v6. Як ви до цього ставитеся?\n\nАргументи ЗА 6v6:\n- Більше командної синергії\n- Менша навантаженість на один танк\n- Ностальгія по OW1\n\nАргументи ЗА 5v5:\n- Менше хаосу\n- Простіше знайти матч\n- Баланс ролей\n\nОсобисто я хочу 6v6 назад. А ви?'},
    {'author': 'frostbyte',   'game': 6, 'title': 'Apex Legends: кращі легенди для рейтингу у сезоні 20', 'content': 'Сезон 20 приніс серйозний шейкап мети. Ось актуальний тірліст:\n\nS-тір: Bloodhound, Wraith, Horizon\nA-тір: Caustic, Lifeline, Gibraltar\nB-тір: Pathfinder, Ash, Seer\nC-тір: Rampart, Mirage, Crypto\n\nBloodhound зараз — абсолютний король мети завдяки пасивному скануванню. Wraith залишається топ вибором для агресивної гри.'},
]

COMMENTS = [
    ('shadowhunter', 0, 'Дякую за поради! Особливо п\'ятий пункт — дуже недооцінений метод навчання.'),
    ('neonviper',    0, 'Повністю погоджуюсь про звук. Колись програв раунд бо не почув кроки за спиною 😅'),
    ('frostbyte',    0, 'Ще б додав: налаштуйте правильно чутливість миші. Це основа всього.'),
    ('galaxystorm',  0, 'А є поради для абсолютних новачків? Я тільки починаю грати.'),
    ('shadowhunter', 0, 'galaxystorm, звісно! Перш за все — вимкни музику в грі і слухай оточення. Це найважливіше.'),

    ('shadowhunter', 1, 'Як саппорт гравець — підписуюся під кожним словом! Роль недооцінена але дуже важлива.'),
    ('ironclad',     1, 'У Dota взагалі командна гра на першому місці. Один хороший саппорт може витягнути всю команду.'),
    ('frostbyte',    1, 'Я ніколи не грав саппорта але після цього поста хочу спробувати!'),

    ('ironclad',     2, 'Дякую за огляд! Чекав його. Нерф Briar справедливий — вона була занадто сильною.'),
    ('shadowhunter', 2, 'А що думаєш про ADC мету? Мені здається зараз вони занадто слабкі.'),
    ('frostbyte',    2, 'ADC потерпіть ще патч — обіцяють апи. Зараз дійсно важко.'),

    ('ironclad',     3, 'Вражаючий проект! Скільки блоків пішло на стіни приблизно?'),
    ('galaxystorm',  3, 'ironclad, рахував — близько 15 тисяч блоків deepslate 😅 Майнив тиждень.'),
    ('neonviper',    3, 'Я теж хочу побудувати щось велике. Можеш поділитися планом будівлі?'),

    ('neonviper',    4, 'Корисний гайд! Ми якраз шукаємо гілера для нашого рейд пулу. Пишіть якщо є бажання.'),
    ('shadowhunter', 4, 'Mythic це інший рівень. Я спробував кілька разів — потрібна дуже злагоджена команда.'),

    ('neonviper',    5, 'Теж погрував на Clove. Дуже цікава механіка після смерті — відчуваєш себе безсмертним 😄'),
    ('galaxystorm',  5, 'Я зовсім не розуміюся на Valorant але відео з Clove виглядають круто!'),

    ('frostbyte',    6, 'Хочу 6v6! 5v5 зробив гру менш цікавою на мою думку.'),
    ('ironclad',     6, 'Мені 5v5 подобається більше. Менше хаосу і краще видно помилки кожного гравця.'),
    ('galaxystorm',  6, 'Не грав OW1 тому не можу порівняти, але 5v5 мені ок.'),

    ('shadowhunter', 7, 'Bloodhound завжди в меті 😄 Дякую за список!'),
    ('neonviper',    7, 'Лайфлайн тепер у A-тірі? Вона ж була нарф кілька сезонів тому...'),
    ('frostbyte',    7, 'neonviper, так, їй підняли ульту — тепер вона знову сильна.'),
]

LFG_POSTS = [
    {'author': 'shadowhunter', 'game': 2, 'role': 'dps',     'rank': 'diamond',  'is_active': True,  'description': 'Шукаю команду для рейтингових матчів у CS2. Граю на позиції entry fragger. Рейтинг Diamond 2, хочу вийти в Master Guardian. Доступний щовечора після 20:00. Мікрофон є, спілкуюся українською або англійською.'},
    {'author': 'neonviper',    'game': 1, 'role': 'support',  'rank': 'platinum', 'is_active': True,  'description': 'Support main з 3000+ годин у Dota 2. Граю на 1-2 позиції. Вмію грати Crystal Maiden, Rubick, Ancient Apparition. Шукаю команду для TI кваліфікацій або просто стабільних рейтингових ігор. Граю кожен день.'},
    {'author': 'frostbyte',    'game': 3, 'role': 'carry',    'rank': 'gold',     'is_active': True,  'description': 'ADC main у League of Legends. Шукаю дуетного партнера — бажано саппорта з мікрофоном. Граю Jinx, Jhin, Caitlyn. Платина 1 минулий сезон, зараз Gold 2. Граю вечорами по будням і весь день у вихідні.'},
    {'author': 'galaxystorm',  'game': 9, 'role': 'any',      'rank': 'any',      'is_active': True,  'description': 'Шукаю друзів для Minecraft! Хочу будувати разом великі проекти на серверах. Casual гравець, граю для розваги. Вік 18+, без токсичності. Є власний приватний сервер.'},
    {'author': 'ironclad',     'game': 8, 'role': 'tank',     'rank': 'any',      'is_active': True,  'description': 'Protection Warrior шукає гільдію для Mythic рейдингу у WoW. Досвід: Clearing Heroic від SL, досвід Mythic+ до 20 ключів. Знаю всі механіки, логи зелені-сині. Шукаю прогрес-орієнтовану але дружню гільдію. Раїджу Вт, Чт, Нд 20:00-23:00.'},
    {'author': 'shadowhunter', 'game': 4, 'role': 'dps',     'rank': 'gold',     'is_active': False, 'description': 'Шукав команду для Valorant. Знайшов — оголошення більше неактивне.'},
]

EVENTS = [
    {
        'author': 'shadowhunter', 'game': 2,
        'title': 'CS2 5v5 Турнір між гравцями TeamForge',
        'description': 'Організовую неофіційний турнір серед учасників платформи!\n\nФормат: 5v5, Single Elimination\nКарти: Mirage, Inferno, Dust2\nПравила: standard competitive\nПриз: звання найкращого гравця місяця 🏆\n\nДля участі потрібен Discord. Деталі у приватних повідомленнях після реєстрації.',
        'days_offset': 7, 'max_players': 10,
        'participants': ['neonviper', 'frostbyte'],
    },
    {
        'author': 'neonviper', 'game': 1,
        'title': 'Dota 2 Inhouse — шукаємо 10 гравців',
        'description': 'Щотижневий Inhouse для гравців TeamForge!\n\nКожен вівторок о 20:00 збираємось і граємо приватні матчі. Формат: Captain\'s Mode.\nРівень: 3000+ MMR бажано, але не обов\'язково.\nГоловне — гарний настрій і командний дух!\n\nПриєднуйтесь — чим більше людей, тим веселіше!',
        'days_offset': 3, 'max_players': 10,
        'participants': ['ironclad', 'shadowhunter'],
    },
    {
        'author': 'frostbyte', 'game': 3,
        'title': 'LoL Duo Queue вечір — Gold+',
        'description': 'Збираємось у Discord і граємо duo queue у League of Legends!\n\nВимоги: Gold і вище, мікрофон, без токсичності.\nЧас: неділя з 15:00\nКількість: до 8 осіб (4 дует-пари)\n\nБудемо рофлити, вчитися і підніматися в рейтингу разом!',
        'days_offset': 5, 'max_players': 8,
        'participants': ['shadowhunter'],
    },
    {
        'author': 'galaxystorm', 'game': 9,
        'title': 'Minecraft Build Battle — хто збудує найкраще місто?',
        'description': 'Запрошую всіх на творчий сервер Minecraft для Build Battle!\n\nТема: Середньовічне місто\nЧас: субота з 14:00 до 18:00\nУчасники голосують за кращу будівлю\nПереможець отримує роль "Архітектор" на сервері\n\nСервер: наданий після реєстрації. Java Edition!',
        'days_offset': 10, 'max_players': 16,
        'participants': ['neonviper', 'ironclad'],
    },
    {
        'author': 'ironclad', 'game': 8,
        'title': 'WoW Heroic Raid — набір до пулу',
        'description': 'Набираємо гравців для Heroic рейдингу у World of Warcraft!\n\nРозклад: Середа та П\'ятниця 20:00-23:00\nВимоги: 470+ ilvl, знання тактик, Discord\nПозиції: потрібні 2 хілера та 1 DPS (ranged)\n\nМи дружній пул без надмірного тиску. Допомагаємо новачкам влитись у рейдинг!',
        'days_offset': 14, 'max_players': 20,
        'participants': ['shadowhunter', 'neonviper', 'frostbyte'],
    },
]


class Command(BaseCommand):
    help = 'Створює демо-дані для TeamForge'

    def handle(self, *args, **kwargs):
        self.stdout.write('Створення користувачів...')
        created_users = {}
        for data in USERS:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={'email': data['email']},
            )
            if created:
                user.set_password('pass1234')
                user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.bio = data['bio']
            profile.discord = data['discord']
            profile.steam = data['steam']
            profile.save()
            games = Game.objects.filter(pk__in=data['games'])
            profile.games.set(games)
            created_users[data['username']] = user
            self.stdout.write(f'  {"Створено" if created else "Вже існує"}: {user.username}')

        self.stdout.write('Створення постів...')
        created_posts = []
        for i, data in enumerate(POSTS):
            author = created_users[data['author']]
            game = Game.objects.get(pk=data['game'])
            post, created = Post.objects.get_or_create(
                author=author, title=data['title'],
                defaults={'content': data['content'], 'game': game},
            )
            created_posts.append(post)
            self.stdout.write(f'  {"+" if created else "="}: {post.title[:50]}')

        self.stdout.write('Створення коментарів...')
        for author_name, post_index, content in COMMENTS:
            author = created_users[author_name]
            post = created_posts[post_index]
            Comment.objects.get_or_create(
                post=post, author=author, content=content,
            )
        self.stdout.write(f'  Додано {len(COMMENTS)} коментарів')

        self.stdout.write('Створення LFG оголошень...')
        for data in LFG_POSTS:
            author = created_users[data['author']]
            game = Game.objects.get(pk=data['game'])
            LFGPost.objects.get_or_create(
                author=author, game=game,
                defaults={
                    'role': data['role'], 'rank': data['rank'],
                    'description': data['description'], 'is_active': data['is_active'],
                },
            )
        self.stdout.write(f'  Додано {len(LFG_POSTS)} LFG оголошень')

        self.stdout.write('Створення подій...')
        for data in EVENTS:
            author = created_users[data['author']]
            game = Game.objects.get(pk=data['game'])
            event, created = Event.objects.get_or_create(
                author=author, title=data['title'],
                defaults={
                    'game': game,
                    'description': data['description'],
                    'event_date': timezone.now() + timedelta(days=data['days_offset']),
                    'max_players': data['max_players'],
                },
            )
            event.participants.add(author)
            for username in data['participants']:
                event.participants.add(created_users[username])
            self.stdout.write(f'  {"+" if created else "="}: {event.title[:50]}')

        self.stdout.write(self.style.SUCCESS('\nГотово! Демо-дані успішно створені.'))
        self.stdout.write('Логін для всіх користувачів: pass1234')
        self.stdout.write('Список користувачів: ' + ', '.join(created_users.keys()))
