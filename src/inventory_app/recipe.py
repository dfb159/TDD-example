"""Recipe API"""

from typing import Mapping


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

    def items(self):
        return self._data.items()


class Recipe:
    """A recipe with ingredients and information about cooking."""
    ingredients: _Ingredients
    time: float
    portions: float

    def __init__(self, *, portions: float, time: float, **ingredients: float):
        self.portions = portions
        self.time = time
        self.ingredients = _Ingredients(ingredients)

    def __getitem__(self, key):
        return self.ingredients[key]

    def for_portions(self, new_portions: float):
        """Scale this recipe to match the given number of portions."""
        factor = new_portions / self.portions
        new_amounts = {n: x*factor for n, x in self.ingredients.items()}
        return Recipe(portions=new_portions, time=self.time, **new_amounts)
