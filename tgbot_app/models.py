from django.db import models


class AppUser(models.Model):
    id = models.BigIntegerField(verbose_name='телеграм id', primary_key=True, unique=True)
    username = models.CharField(verbose_name='имя пользователя', max_length=32, blank=True, null=True)
    name = models.CharField(verbose_name='имя', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    def __str__(self):
        return f'<User: {self.id}({self.username})>'


class UserSession(models.Model):
    user = models.ForeignKey(AppUser, verbose_name='пользователь', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='наименование товара', max_length=255, blank=True, null=True)
    description = models.TextField(verbose_name='описание товара', blank=True, null=True)
    characteristics = models.JSONField(verbose_name='характеристики товара', blank=True, null=True)
    sku_plus = models.CharField(verbose_name='дополнительные SCU', max_length=100, blank=True, null=True)
    seo_dict = models.TextField(verbose_name='SEO словарь', blank=True, null=True)
    seo_phrases = models.TextField(verbose_name='SEO фразы', blank=True, null=True)
    seo_user = models.TextField(verbose_name='пользовательские SEO слова', blank=True, null=True)
    minus_words = models.TextField(verbose_name='минус слова', blank=True, null=True)
    important = models.TextField(verbose_name='важное о товаре', blank=True, null=True)
    style = models.CharField(verbose_name='стиль', max_length=15, default='regular')
    is_updated = models.BooleanField(verbose_name='обновлена', default=False)
    is_active = models.BooleanField(verbose_name='открыта', default=True)
    created_at = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    def update_field(self, field, new_value):
        self.__setattr__(field, new_value)


class Message(models.Model):
    user_session = models.ForeignKey(UserSession, verbose_name='сессия', on_delete=models.CASCADE)
    is_user = models.BooleanField(verbose_name='сообщение от пользователя', default=True)
    is_active = models.BooleanField(verbose_name='текущий', default=True)
    text = models.TextField(verbose_name='сообщение')
    created_at = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    def __str__(self):
        return f'<Message: {self.id}({self.user_session})>'

    class Meta:
        ordering = ['created_at']


class SeoWB(models.Model):
    phrase = models.CharField(verbose_name='фраза', max_length=255)
    lemmas = models.CharField(verbose_name='нормализованная фраза', max_length=255)
    frequency = models.BigIntegerField(verbose_name='частота')
    created_at = models.DateField(verbose_name='дата добавления')

