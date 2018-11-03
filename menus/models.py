from django.db import models
from recipes.models import Recipe
from collections import defaultdict
from math import ceil

# Create your models here.
class Menu(models.Model):
    name = models.TextField()
    recipes = models.ManyToManyField(Recipe, related_name="menus")
    servings = models.IntegerField()

    def __str__(self):
        return ("{}\n{}\nfor {}\n".format(self.name, '='*len(self.name), self.servings) + 
            "\n".join(" - {} * {}".format(ceil(self.servings/r.servings), r) for r in self.recipes.all()))

    def __repr__(self):
        return "<{} with {} recipes>".format(self.name, self.recipes.count())

    def shopping_list(self):
        shop = defaultdict(float)
        for recipe in self.recipes.all():
            scale = ceil(self.servings / recipe.servings)
            print("Scaling {} by {}".format(recipe, scale))
            for ri in recipe.ingredients.all():
                try:
                    shop[(ri.ingredient, ri.convert().unit)] = scale * ri.convert().quantity
                except ValueError:
                    shop[(ri.ingredient, ri.unit)] = scale * ri.quantity
        for (ing, unit), qty in shop.items():
            print(" - {} {} of {}".format(qty, unit, ing))

    def cooking_view(self):
        print(self.name)
        print("="*80)
        print("to serve {}".format(self.servings))
        for r in self.recipes.all():
            scale = ceil(self.servings / r.servings)
            print(" - {} * {}".format(scale, r))
            for ri in r.ingredients.all():
                print("   - {} {} {}{}".format(
                    ri.quantity * scale,
                    ri.unit,
                    ri.ingredient,
                    ' (' + ri.notes + ')' if ri.notes else ''
                ))
        print('')
        for r in self.recipes.all():
            print('-'*80)
            print(r)
            for step in r.steps.all():
                print("  - " + step.description)
                
        
