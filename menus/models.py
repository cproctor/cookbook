from django.db import models
from recipes.models import Recipe
from collections import defaultdict
from math import ceil
from textwrap import TextWrapper

# Create your models here.
class Menu(models.Model):
    name = models.TextField()
    recipes = models.ManyToManyField(Recipe, related_name="menus")
    servings = models.IntegerField()

    def __str__(self, width=70):
        wrapper = TextWrapper(width=width)
        listWrapper = TextWrapper(width=width, initial_indent=' - ', subsequent_indent='   ')
        text = []
        text += wrapper.wrap(self.name)
        text.append('='*width)
        text.append("to serve {}".format(self.servings))
        for r in self.recipes.all():
            text += listWrapper.wrap("{} * {}".format(ceil(self.servings/r.servings), r))
        return "\n".join(text)

    def __repr__(self):
        return "<{} with {} recipes>".format(self.name, self.recipes.count())

    def shopping_list(self, width=70):
        wrapper = TextWrapper(width=width)
        listWrapper = TextWrapper(width=width, initial_indent=' - ', subsequent_indent='   ')
        text = []
        text.append(self.__str__(width))
        text.append('-'*width)
        shop = defaultdict(float)
        for recipe in self.recipes.all():
            scale = ceil(self.servings / recipe.servings)
            for ri in recipe.ingredients.all():
                print(ri, scale)
                try:
                    shop[(ri.ingredient, ri.convert().unit)] += scale * ri.convert().quantity
                except ValueError:
                    shop[(ri.ingredient, ri.unit)] += scale * ri.quantity
        for (ing, unit), qty in shop.items():
            text += listWrapper.wrap("{} {} of {}".format(qty, unit, ing))
        for line in text:
            print(line)

    def cooking_view(self, width=70):
        wrapper = TextWrapper(width=width)
        listWrapper = TextWrapper(width=width, initial_indent=' - ', subsequent_indent='   ')
        subListWrapper = TextWrapper(width=width, initial_indent='   - ', subsequent_indent='     ')
        text = []
        text.append(self.__str__(width))
        text.append('-'*width)
        text.append("Ingredients")
        for r in self.recipes.all():
            scale = ceil(self.servings / r.servings)
            text += listWrapper.wrap("{} * {}".format(scale, r))
            for ri in r.ingredients.all():
                text += subListWrapper.wrap("{} {} {}{}".format(
                    ri.quantity * scale,
                    ri.unit,
                    ri.ingredient,
                    ' (' + ri.notes + ')' if ri.notes else ''
                ))
        for r in self.recipes.all():
            text.append('-'*width)
            text += wrapper.wrap(r.name)
            for step in r.steps.all():
                text += listWrapper.wrap(step.description)
        for line in text:
            print(line)
                
    class Meta:
        ordering=['name']
