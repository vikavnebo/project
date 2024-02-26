from django.views.generic import TemplateView

from menu.models import Item


class IndexPage(TemplateView):
    template_name = "menu/index.html"


class Menu(TemplateView):
    template_name = "menu/index.html"
