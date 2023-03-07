from django.db import models


class AppUser(models.Model):
    id = models.PositiveIntegerField(verbose_name='телеграм id', primary_key=True, unique=True)
    username = models.CharField(verbose_name='имя пользователя', max_length=32, unique=True)
    name = models.CharField(verbose_name='имя', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    def __str__(self):
        return f'<User: {self.id}({self.username})>'


class UserSession(models.Model):
    user = models.ForeignKey(AppUser, verbose_name='пользователь', on_delete=models.PROTECT)
    product_title = models.CharField(verbose_name='наименование товара', max_length=255)
    product_description = models.TextField(verbose_name='описание товара')
    product_characteristics = models.JSONField(verbose_name='характеристики товара')
    other_descriptions_1 = models.TextField(verbose_name='дополнительные описания 1', blank=True, null=True)
    other_descriptions_2 = models.TextField(verbose_name='дополнительные описания 2', blank=True, null=True)
    other_descriptions_3 = models.TextField(verbose_name='дополнительные описания 3', blank=True, null=True)
    seo_dict = models.TextField(verbose_name='SEO словарь', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='открыта', default=True)
    created_at = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    def __str__(self):
        return f'<Session: {self.id}({self.product_title})>'


class Message(models.Model):
    user_session = models.ForeignKey(UserSession, verbose_name='сессия', on_delete=models.PROTECT)
    is_answer = models.BooleanField(verbose_name='chatGPT', default=False)
    text = models.TextField(verbose_name='сообщение')
    created_at = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    def __str__(self):
        return f'<Message: {self.id}({self.user_session})>'

    class Meta:
        ordering = ['created_at']
