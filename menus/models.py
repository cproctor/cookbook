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

    def __str__(self, width=70, format=None):
        if format == "markdown":
            return "\n# {}\n\n## Recipes (to serve {})\n\n{}".format(
                self.name, 
                self.servings, 
                '\n'.join([" - {} * {}".format(ceil(self.servings/r.servings), r) for r in self.recipes.all()])
            )

        elif format is None:
            wrapper = TextWrapper(width=width)
            listWrapper = TextWrapper(width=width, initial_indent=' - ', subsequent_indent='   ')
            text = []
            text += wrapper.wrap(self.name)
            text.append('='*width)
            text.append("to serve {}".format(self.servings))
            for r in self.recipes.all():
                text += listWrapper.wrap("{} * {}".format(ceil(self.servings/r.servings), r))
            return "\n".join(text)

        else:
            raise ValueError("If given, format must be one of {}".format(", ".join(self.formats)))

    def __repr__(self):
        return "<{} with {} recipes>".format(self.name, self.recipes.count())

    def shopping_list(self, width=70):
        wrapper = TextWrapper(width=width)
        listWrapper = TextWrapper(width=width, initial_indent=' - ', subsequent_indent='   ')
        text = []
        text.append(self.__str__(width))
        text.append('-'*width)
        for (ing, unit), qty in self.get_shopping_items().items():
            text += listWrapper.wrap("{} {} of {}".format(qty, unit, ing))
        for line in text:
            print(line)

    def shopping_csv(self):
        "Prints a shopping list as a CSV"
        print("ingredient,unit,quantity")
        for (ing, unit), qty in self.get_shopping_items().items():
            print("{},{},{}".format(ing, unit, qty))

    def get_shopping_items(self):
        "Returns a dict of shopping items"
        shop = defaultdict(float)
        for recipe in self.recipes.all():
            scale = ceil(self.servings / recipe.servings)
            for ri in recipe.ingredients.all():
                try:
                    shop[(ri.ingredient, ri.convert().unit)] += scale * ri.convert().quantity
                except ValueError:
                    shop[(ri.ingredient, ri.unit)] += scale * ri.quantity
        return shop

    formats = ["markdown"]

    def cooking_view(self, format=None, width=70):
        if format:
            if format not in self.formats:
                raise ValueError("Format must be one of {}".format(", ".join(self.formats)))
            if format == "markdown":
                return self.cooking_view_markdown()
            
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
            scale = ceil(self.servings / r.servings)
            text.append('-'*width)
            text += wrapper.wrap(r.name)
            for step in r.steps.all():
                text += listWrapper.wrap(step.scaled_description(scale))
        for line in text:
            print(line)

    def cooking_view_markdown(self):
        text = []
        text.append(self.__str__(format="markdown"))
        text.append("\n## Ingredients\n")
        for r in self.recipes.all():
            scale = ceil(self.servings / r.servings)
            text.append(" - {} * {}".format(scale, r))
            for ri in r.ingredients.all():
                text.append("   - {} {} {}{}".format(
                    ri.quantity * scale,
                    ri.unit,
                    ri.ingredient,
                    ' (' + ri.notes + ')' if ri.notes else ''
                ))
        text.append("\n## Steps")
        for r in self.recipes.all():
            scale = ceil(self.servings / r.servings)
            text.append("\n### " + r.name + '\n')
            for step in r.steps.all():
                text.append(' - ' + step.scaled_description(scale))
        for line in text:
            print(line)
        


    class Meta:
        ordering=['name']
