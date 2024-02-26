from django.contrib import admin

from .models import *


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	list_display = ('name', 'url')
	list_editable = ('url',)


@admin.register(Item)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'url', 'menu', 'parent')
	list_editable = ('url', 'menu', 'parent')
	list_filter = ('menu', 'parent')
