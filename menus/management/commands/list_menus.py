from django.core.management.base import BaseCommand, CommandError
from menus.models import Menu
from recipes.models import Recipe, Ingredient

class Command(BaseCommand):
    help = "List menus"

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='?', help="Filter by name")
        parser.add_argument("-r", "--recipes", nargs='+', help="Show menus with these recipes")

    def handle(self, *args, **options):
        menus = Menu.objects.all()
        if options['name']:
            menus = menus.filter(name__contains=options['name'])
        if options['recipes']:
            for recipe_name in options['recipes']:
                menus = menus.filter(recipes__name__contains=recipe_name)
        if any(menus):
            for menu in menus:
                print(menu)
        else:
            print("No menus matched the search")
