from django.utils.html import format_html

from App.settings.labels_with_svg import black_list_with_icon
from App.settings.labels_with_svg import block_label_with_icon
from App.settings.labels_with_svg import email_label_with_icon
from App.settings.labels_with_svg import log_label_with_icon
from App.settings.labels_with_svg import notification_with_icon
from App.settings.labels_with_svg import profile_label_with_icon
from App.settings.labels_with_svg import redoc_label_with_icon
from App.settings.labels_with_svg import suggestion_label_with_icon
from App.settings.labels_with_svg import swagger_label_with_icon
from App.settings.labels_with_svg import user_label_with_icon


"""
JET Documentation: https://django-jet-reboot.readthedocs.io/
"""

JET_SIDE_MENU_COMPACT = True
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default',  # theme title
    },
    {'theme': 'green', 'color': '#44b78b', 'title': 'Green'},
    {'theme': 'light-green', 'color': '#2faa60', 'title': 'Light Green'},
    {'theme': 'light-violet', 'color': '#a464c4', 'title': 'Light Violet'},
    {'theme': 'light-blue', 'color': '#5EADDE', 'title': 'Light Blue'},
    {'theme': 'light-gray', 'color': '#222', 'title': 'Light Gray'},
]
JET_SIDE_MENU_ITEMS = [
    {
        'label': ('People'),
        'app_label': 'Users',
        'items': [
            {'name': 'user', 'label': format_html(user_label_with_icon)},
            {'name': 'profile', 'label': format_html(profile_label_with_icon)},
        ],
    },
    {
        'label': ('Email'),
        'app_label': 'Emails',
        'items': [
            {
                'name': 'suggestion',
                'label': format_html(suggestion_label_with_icon),
            },
            {'name': 'email', 'label': format_html(email_label_with_icon)},
            {
                'name': 'notification',
                'label': format_html(notification_with_icon),
            },
            {'name': 'block', 'label': format_html(block_label_with_icon)},
            {'name': 'blacklist', 'label': format_html(black_list_with_icon)},
        ],
    },
    {
        'label': ('Adminitsration'),
        'app_label': 'admin',
        'items': [
            {'name': 'logentry', 'label': format_html(log_label_with_icon)}
        ],
    },
    {
        'label': 'Documentation',
        'items': [
            {
                'label': format_html(swagger_label_with_icon),
                'url': '/docs/swagger/',
                'url_blank': True,
            },
            {
                'label': format_html(redoc_label_with_icon),
                'url': '/docs/redoc/',
                'url_blank': True,
            },
        ],
    },
    {
        'label': ('Others'),
        'items': [
            {
                'label': 'Grafana',
                'url': 'http://localhost:3000/',
                'url_blank': True,
            },
            {
                'label': 'Prometheus',
                'url': 'http://localhost:9090/',
                'url_blank': True,
            },
            {
                'label': 'RabbitMQ',
                'url': 'http://localhost:15672/',
                'url_blank': True,
            },
            {
                'label': 'Flower',
                'url': 'http://localhost:5555/',
                'url_blank': True,
            },
            {
                'label': 'CloudBeaver',
                'url': 'http://localhost:8081/',
                'url_blank': True,
            },
        ],
    },
]
