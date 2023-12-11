"""
Recipe API.

This module contains the implementation of the Recipe class, which represents a recipe with ingredients and information about cooking.
"""

from typing import Mapping, Self


class _Ingredients(Mapping):
    _data: dict[str, float]

    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __eq__(self, other: Self | dict[str, float]):
        if isinstance(other, dict):
            return self._data == other
        elif isinstance(other, _Ingredients):
            return self._data == other._data
        else:
            return NotImplemented

    def items(self):
        """Return an iterator over the items in this recipe."""
        return self._data.items()


class Recipe:
    """A recipe with ingredients and information about cooking.

    Attributes:
        ingredients (dict): A dictionary containing the ingredients and their quantities.
        time (float): The cooking time for the recipe.
        portions (float): The number of portions the recipe yields.

    Methods:
        for_portions(self, new_portions: float): Scales the recipe to match a given number of portions.
    """

    ingredients: _Ingredients
    """A dictionary containing the ingredients and their quantities."""

    time: float
    """The cooking time for the recipe."""

    portions: float
    """The number of portions the recipe yields."""

    def __init__(self, *, portions: float, time: float, **ingredients: float):
        """
        Initialize a Recipe object.

        Arguments:
            portions (float): The number of portions the recipe yields.
            time (float): The time required to prepare the recipe.
            **ingredients (float): The ingredients required for the recipe, along with their quantities.

        Returns:
            None
        """
        self.portions = portions
        self.time = time
        self.ingredients = _Ingredients(ingredients)

    def __getitem__(self, key):
        return self.ingredients[key]

    def __eq__(self, other: Self | dict[str, float]):
        if isinstance(other, dict):
            return self.ingredients == other
        elif isinstance(other, Recipe):
            return self.ingredients == other.ingredients
        else:
            return NotImplemented

    def for_portions(self, new_portions: float):
        """
        Create a new Recipe object with adjusted ingredient amounts for the specified number of portions.

        Arguments:
            new_portions (float): The desired number of portions for the new Recipe.

        Returns:
            Recipe: A new Recipe object with adjusted ingredient amounts for the specified number of portions.
        """
        factor = new_portions / self.portions
        new_amounts = {n: x * factor for n, x in self.ingredients.items()}
        return Recipe(portions=new_portions, time=self.time, **new_amounts)
