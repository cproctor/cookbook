from django.test import TestCase
from recipes.models import *
from recipes.importers import YAMLRecipeImporter

class IngredientUnitTestCase(TestCase):
    def setUp(self):
        self.T = IngredientUnit.objects.get(short='T')

    def test_finds_conversions(self):
        # for unit, scale in self.T.possible_conversions().items():
            # print("{} = {} * {}".format(unit, self.T, scale))
        self.assertEqual(len(self.T.possible_conversions()), 6)
        

class ImporterTestCase(TestCase):
    def test_imports(self):
        importer = YAMLRecipeImporter()
        importer.import_recipe("recipes/fixtures/japanese_turnips.yaml")
        self.assertEqual(Ingredient.objects.count(), 3)
