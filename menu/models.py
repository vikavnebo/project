from django.db import models
from django.urls import reverse


class UsedItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(menu__isnull=True)


class Menu(models.Model):
    name = models.CharField(verbose_name='Menu name', max_length=30, unique=True)
    url = models.SlugField(verbose_name="Menu url", max_length=30, unique=True)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(verbose_name='Item name', max_length=30, unique=True)
    url = models.SlugField(verbose_name="Item url", max_length=30, unique=True)
    menu = models.ForeignKey(Menu, blank=True, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    children = list()

    objects = models.Manager()
    used = UsedItemManager()

    class Meta:
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu', kwargs={'item_url': self.url})
