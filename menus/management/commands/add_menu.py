from django.core.management.base import BaseCommand, CommandError
from menus.models import Menu
from recipes.models import Recipe, Ingredient

class Command(BaseCommand):
    help = "Add a menu"

    def add_arguments(self, parser):
        parser.add_argument('name', help="Menu name")
        parser.add_argument('servings', type=int, help="Number of servings")
        parser.add_argument("-r", "--recipes", nargs='+', help="Recipes in the menu")

    def handle(self, *args, **options):
        try:
            menu = Menu(name=options['name'], servings=options['servings'])
            menu.save()
            for recipe_name in options['recipes']:
                menu.recipes.add(Recipe.get_by_name(recipe_name))
        except (Recipe.DoesNotExist, Recipe.MultipleObjectsReturned):
            menu.delete()
            raise CommandError("No recipe with name '{}'".format(recipe_name))
        except Recipe.MultipleObjectsReturned:
            menu.delete()
            raise CommandError("Multiple recipes matched name '{}'".format(recipe_name))
