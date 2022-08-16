from django.db import models
from django.urls import reverse


class MovieInformation(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    video_url = models.CharField(max_length=255, db_index=True, verbose_name="Video_URL")
    content = models.TextField(blank=True, verbose_name="Аннотация")
    photo = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('MovieUniverses', on_delete=models.PROTECT, verbose_name="Вселенная")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-time_create', 'title']


class MovieUniverses(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Вселенная")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('universe', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Киновселенная'
        verbose_name_plural = 'Киновселенные'
        ordering = ['id']


class Comment(models.Model):
    post = models.ForeignKey(MovieInformation, on_delete=models.DO_NOTHING, verbose_name="Фильм")
    name = models.CharField(max_length=80, verbose_name="Логин")
    email = models.EmailField()
    body = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Комментарий от {}, {}'.format(self.name, self.post, self.body)

    def get_absolute_url(self):
        return reverse('comment', kwargs={'com_post': self.post})
