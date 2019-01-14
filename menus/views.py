from django.shortcuts import render
from django.views import generic
from menus.models import Menu

# Create your views here.
class IndexView(generic.ListView):
    model = Menu
    template_name = 'menus/index.html'
    context_object_name = 'menus'
