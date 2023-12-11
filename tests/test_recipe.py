"""Unit tests for the Recipe class."""
from inventory_app.recipe import Recipe
from pytest import raises


def test__recipe_ingredients_equality():
    """Check the equality between recipe.ingredients and direct dictionary."""
    recipe = Recipe(portions=4, time=45, sugar=1, flour=2, milk=0.25)
    assert recipe.ingredients == {"sugar": 1, "flour": 2, "milk": 0.25}


def test__recipe_equality():
    """Check the equality between recipe and direct dictionary."""
    recipe = Recipe(portions=4, time=45, sugar=1, flour=2, milk=0.25)
    assert recipe == {"sugar": 1, "flour": 2, "milk": 0.25}


def test__recipe_ingredient_access():
    """Accessing recipe ingredients should return the correct quantities."""
    recipe = Recipe(portions=4, time=45, sugar=1, flour=2, milk=0.25)
    assert recipe["sugar"] == 1
    assert recipe["flour"] == 2
    assert recipe["milk"] == 0.25


def test__recipe_ingredient_assignment():
    """Cannot update the ingredients of a recipe."""
    recipe = Recipe(portions=4, time=45, sugar=1, flour=2, milk=0.25)

    with raises(TypeError, match="'Recipe' object does not support item assignment"):
        recipe["sugar"] = 2

    with raises(TypeError, match="'_Ingredients' object does not support item assignment"):
        recipe.ingredients["sugar"] = 2


def test__recipe_for_portions():
    """Creating a new recipe with adjusted portions should scale the ingredients."""
    recipe = Recipe(portions=4, time=45, sugar=1, flour=2, milk=0.25)
    new_recipe = recipe.for_portions(6)
    assert new_recipe == {"sugar": 1.5, "flour": 3, "milk": 0.375}
    assert new_recipe.time == 45
    assert new_recipe.portions == 6
