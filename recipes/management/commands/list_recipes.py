from django.core.management.base import BaseCommand, CommandError
from recipes.models import Recipe, Ingredient

class Command(BaseCommand):
    help = "List all recipes"

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='?', help="Filter by name")
        parser.add_argument("-i", "--ingredients", nargs='+', 
                help="Show recipes with all these ingredients")

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        if options['name']:
            recipes=recipes.filter(name__contains=options['name'])
        if options['ingredients']:
            for name in options['ingredients']:
                recipes=recipes.filter(ingredients__ingredient__name__contains=name)
        if any(recipes):
            for recipe in recipes:
                print(recipe)
        else:
            print("No recipes matched the search")
