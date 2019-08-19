from django.core.management.base import BaseCommand, CommandError
import yaml
from recipes.importers import RecipeImporter
from recipes.models import Recipe
from menus.models import Menu

class Command(BaseCommand):
    help = "Display a shopping list for a menu. Provide a menu name or list the recipes"

    def add_arguments(self, parser):
        parser.add_argument("menu", nargs='?', help="Name of menu (fuzzy match)")
        parser.add_argument("-r", "--recipes", nargs="*", help="Names of recipes (fuzzy match)")
        parser.add_argument("-s", "--servings", type=int, help="Number of people to serve")

    def handle(self, *args, **options):
        if not options['menu'] and not options['recipes']:
            raise CommandError("Please provide a menu name or a list or recipes.")
        if options['menu']:
            if options['recipes']:
                raise CommandError("Please provide a menu name or a list of recipes, but not both.")
            menu = Menu.objects.get(name__contains=options['menu'])
            if options['servings']:
                menu.servings = options['servings']
            menu.cooking_view()
        else:
            try:
                recipes = [Recipe.get_by_name(name, ask_which=True) for name in options['recipes']]
            except (Recipe.DoesNotExist, Recipe.MultipleObjectsReturned) as e:
                raise CommandError(e)
            tempMenu = Menu(name="Menu", servings=options['servings'] or 1)
            tempMenu.save()
            tempMenu.recipes.set(recipes)
            tempMenu.cooking_view()
            tempMenu.delete()

