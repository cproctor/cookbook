from django.db import models
from django.db.models import Q
from collections import deque
from recipes.helpers import choose_from_options
import re

class RecipeTag(models.Model):
    name = models.CharField(max_length=200, unique=True)

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    source = models.URLField()
    servings = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(RecipeTag, related_name='recipes')
    stepsAndIngredients = models.CharField(max_length=5000)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_name(self, name, ask_which=False):
        "Looks up a recipe by fuzzy-matched name, handling errors with informative messages"
        try:
            return Recipe.objects.get(name__contains=name)
        except Recipe.DoesNotExist:
            raise Recipe.DoesNotExist("No recipe found with name '{}'".format(name))
        except Recipe.MultipleObjectsReturned:
            if ask_which:
                prompt = f"Multiple recipes matched '{name}'. Which did you mean?"
                matches = Recipe.objects.filter(name__contains=name).all()
                return choose_from_options(matches, [r.name for r in matches], prompt)
            else:
                raise Recipe.MultipleObjectsReturned("More than one recipe found with name '{}'".format(name))

    class Meta:
        ordering=['name']

class IngredientCategory(models.Model):
    name = models.CharField(max_length=100)

class IngredientUnitConversion(models.Model):
    source = models.ForeignKey("IngredientUnit", on_delete=models.CASCADE, related_name="conversions")
    target = models.ForeignKey("IngredientUnit", on_delete=models.CASCADE)
    scale = models.FloatField()
    allowed_ingredients = models.ManyToManyField("Ingredient")

    def __str__(self, short=False):
        if self.allowed_ingredients.exists():
            return "{} * {} -> {} [{}]".format(self.source.__str__(short), self.scale, self.target.__str__(short), ", ".join(self.allowed_ingredients))
        else:
            return "{} * {} -> {}".format(self.source.__str__(short), self.scale, self.target.__str__(short))

class IngredientUnit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short = models.CharField(max_length=100, unique=True)
    convertable_units = models.ManyToManyField(
        "IngredientUnit",
        through="IngredientUnitConversion",
        through_fields=("source", "target")
    )

    @classmethod
    def lookup(cls, key):
        try:
            return IngredientUnit.objects.get(name=key)
        except IngredientUnit.DoesNotExist:
            return IngredientUnit.objects.get(short=key)

    def __str__(self, short=False):
        return self.short if short else self.name

    def conversion_scale(self, target, ingredient=None):
        "Given a target unit, tries to find a conversion to the target. Returns scale or None."
        try:
            return self.conversions.get(target=target).scale
        except IngredientUnitConversion.DoesNotExist:
            return dict(self.possible_conversions(ingredient)).get(target)

    def possible_conversions(self, ingredient=None):
        "Returns recursive {unit: scale} conversions for ingredient"
        result = {self:1}
        edges = deque([self])
        while any(edges):
            unit = edges.popleft()
            newConversions = unit.conversions.filter(
                (Q(allowed_ingredients=None) |
                Q(allowed_ingredients=ingredient)) &
                ~Q(target_id__in=[c.id for c in result.keys()])
            ).all()
            for conv in newConversions:
                result[conv.target] = result[unit] * conv.scale
                if conv.target not in edges:
                    edges.append(conv.target)
        del result[self]
        return result

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(IngredientCategory, related_name='ingredients',
            null=True, blank=True, on_delete=models.CASCADE)
    canonicalUnit = models.ForeignKey(IngredientUnit, on_delete=models.CASCADE,
            null=True, blank=True)
    recipes=models.ManyToManyField(Recipe, through='RecipeIngredient', through_fields=('ingredient', 'recipe'))

    def __str__(self):
        return self.name

    def unit(self):
        return self.canonicalUnit or self.recipeingredient_set.first().unit

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.ForeignKey(IngredientUnit, on_delete=models.CASCADE)
    quantity = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} {} of {}{}".format(
            self.quantity,
            self.unit,
            self.ingredient,
            " ({})".format(self.notes) if self.notes else ""
        )

    def convert(self, targetUnit=None):
        targetUnit = targetUnit or self.ingredient.unit()
        if targetUnit == self.unit: return self
        conversionScale = self.unit.conversion_scale(targetUnit)
        if conversionScale is None:
            raise ValueError("Cannot convert '{}' to '{}'".format(self.unit, targetUnit))
        return RecipeIngredient(
            recipe=self.recipe,
            ingredient=self.ingredient,
            unit=targetUnit,
            quantity=self.quantity * conversionScale,
            notes=self.notes
        )

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)
    description = models.TextField()

    def scaled_description(self, scale):
        pattern = "\{([^,]+),([^,]+),([^,]+)\}"
        step = self.description
        while True:
            m = re.search(pattern, step)
            if not m:
                break
            qty, unit, ing = m.groups()
            step = re.sub(pattern, "{} {} {}".format(float(qty) * scale, unit.strip(), ing.strip()), step)
        return step

    def __str__(self):
        return self.description
