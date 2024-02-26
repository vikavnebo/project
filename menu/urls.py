from django.urls import path

from .views import *


urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('<slug:item_url>/', Menu.as_view(), name='menu'),
]
