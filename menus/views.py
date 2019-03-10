from django.shortcuts import render
from django.views import generic
from menus.models import Menu
from django.http import Http404

# Create your views here.
class IndexView(generic.ListView):
    model = Menu
    template_name = 'menus/index.html'
    context_object_name = 'menus'

class DetailView(generic.DetailView):
    model = Menu
    template_name = 'menus/detail.html'

class MenuRecipeDetailView(generic.DetailView):
    template_name = 'menus/menu_recipe_detail.html'

    def get_object(self):
        try:
            self.menu = Menu.objects.get(pk=self.kwargs['menuID'])
            self.recipe = self.menu.recipes.get(pk=self.kwargs['recipeID'])
            return self.recipe
        except (Menu.DoesNotExist, Recipe.DoesNotExist):
            raise Http404("Sorry, couldn't find it.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.menu
        context['recipe'] = self.recipe
        return context

    
