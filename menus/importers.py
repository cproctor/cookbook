from recipes.models import Recipe
from menus.models import Menu
from common.logs import get_logger
import logging
import yaml

class MenuImporter:
    """
    Imports a data structure as a menu. Recipes will be added as fuzzy match. 
    {
        name: str,
        servings: int,
        recipes: [str]
    }
    """
    def __init__(self, log=None):
        self.log = log or get_logger(__file__, "menu_importer.log", logging.WARNING)

    def import_menu(self, data):
        r = [Recipe.get_by_name(name, ask_which=True) for name in data['recipes']]
        self.m = Menu(
            name=data['name'],
            servings=data['servings']
        )
        self.m.save()
        self.m.recipes.set(r)
        self.log.info("Created menu {}".format(self.m))

class YAMLMenuImporter(MenuImporter):
    def import_menu(self, path):
        with open(path) as menuFile:
            super().import_menu(yaml.load(menuFile.read()))

