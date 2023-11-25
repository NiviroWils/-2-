from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [
        ('Н', 'Новая'),
        ('П', 'Принято в работу'),
        ('В', 'Выполнено')
    ]
    created = models.DateTimeField(auto_now_add=True, verbose_name='Временная метка заявки')
    title = models.CharField(max_length=255, verbose_name='Название заявки')
    description = models.TextField(verbose_name='Описание заявки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория заявки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name='Статус заявки')
    image = models.ImageField(upload_to='images/', verbose_name='Фото помещения или план заявки')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заявитель')
    image_done = models.ImageField(upload_to='images_done/', blank=True, verbose_name='Созданный дизайн')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.title
