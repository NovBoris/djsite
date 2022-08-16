from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}
]
button = {'title': "Добавить комментарий", 'url_name': 'add_comment'}


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = MovieUniverses.objects.annotate(Count('movieinformation'))
            cache.set('cats', cats, 60)
        user_menu = menu.copy()
        context['button'] = button
        if not self.request.user.is_authenticated:
            user_menu.pop(0)
            del context['button']

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context
