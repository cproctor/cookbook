from django.core.management.base import BaseCommand, CommandError
import yaml
from recipes.importers import RecipeImporter, get_logger, get_log_level
from django.core.management import call_command
from pathlib import Path

class Command(BaseCommand):
    help = "Import all recipes into the database"
    database = 'db.sqlite3'

    def add_arguments(self, parser):
        parser.add_argument('-p', "--recipes_path", default='recipe_sources')
        parser.add_argument('-f', '--force', action='store_true', help="Rebuild the database from recipe_sources")
        parser.add_argument('-e', '--log_level', default='warning')

    def handle(self, *args, **options):
        if options['force']:
            Path(self.database).unlink()
            call_command('migrate')

        loglevel = get_log_level(options['log_level'])
        logger = get_logger(__file__, "recipe_importer.log", loglevel)
        importer = RecipeImporter(logger)
        for f in Path(options['recipes_path']).glob('*.yaml'):
            with open(f) as inf:
                importer.import_recipe(yaml.load(inf.read()))
        


