from django.core.management.base import BaseCommand, CommandError
import yaml
from recipes.importers import RecipeImporter
from pathlib import Path

class Command(BaseCommand):
    help = "Import all recipes into the database"

    def add_arguments(self, parser):
        parser.add_argument('-p', "--recipes_path", default='recipe_sources')

    def handle(self, *args, **options):
        importer = RecipeImporter()
        for f in Path(options['recipes_path']).glob('*.yaml'):
            with open(f) as inf:
                importer.import_recipe(yaml.load(inf.read()))
        


