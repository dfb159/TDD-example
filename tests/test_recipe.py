"""Tests for the basic Inventory API."""


from inventory_app.recipe import Recipe


def test__recipe_contains_information():
    """A newly instanciated recipe should persist information from constructor."""
    recipe = Recipe(portions=2, time=30, sugar=2, flour=3, milk=0.5)
    assert len(recipe.ingredients) == 3
    assert recipe["sugar"] == 2
    assert recipe["flour"] == 3
    assert recipe["milk"] == 0.5
    assert recipe.portions == 2
    assert recipe.time == 30


def test__recipe_portions_scale():
    """Scaling a recipe should scale ingredients, but not time."""
    recipe = Recipe(portions=2, time=30, sugar=2, flour=3, milk=0.5)
    scaled = recipe.for_portions(3)
    assert scaled["sugar"] == 3
    assert scaled["flour"] == 4.5
    assert scaled["milk"] == 0.75
    assert scaled.time == 30
    assert scaled.portions == 3
