from django.core.management.base import BaseCommand, CommandError
import yaml
from menus.importers import YAMLMenuImporter

class Command(BaseCommand):
    help = "Import a menu into the database from a yaml file"

    def add_arguments(self, parser):
        parser.add_argument("menu_file")

    def handle(self, *args, **options):
        importer = YAMLMenuImporter()
        importer.import_menu(options['menu_file'])
