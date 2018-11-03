from django.core.management.base import BaseCommand, CommandError
import yaml
from recipes.importers import RecipeImporter

class Command(BaseCommand):
    help = "Import a recipe into the database"

    def add_arguments(self, parser):
        parser.add_argument("recipe_file")

    def handle(self, *args, **options):
        importer = RecipeImporter()
        with open(options['recipe_file']) as inf:
            importer.import_recipe(yaml.load(inf.read()))
        

