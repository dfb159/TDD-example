"""Unit tests for the CookingService class."""
from pytest import raises
from inventory_app.inventory import Inventory
from inventory_app.recipe import Recipe
from inventory_app.cooking_service import CookingException, CookingService


def test__recipe_ingredients_availiable():
    """The ingredients of a recipe are availiable in the inventory."""
    inventory = Inventory(milk=5, flour=3, sugar=2, noodles=4)
    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)

    cooking_service = CookingService(inventory)
    assert cooking_service.is_cookable(cookies)


def test__recipe_ingredients_not_enough():
    """The ingredients of a recipe are not availiable in the inventory."""
    inventory = Inventory(milk=5, flour=3, sugar=2, noodles=4)
    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=4)

    cooking_service = CookingService(inventory)
    assert not cooking_service.is_cookable(cookies)


def test__cooking_a_recipe():
    """The ingredients are substracted on cooking."""
    inventory = Inventory(milk=2, flour=4, sugar=5, noodles=4)
    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)

    cooking_service = CookingService(inventory)
    cooking_service.cook_recipe(cookies)

    assert inventory == {"milk": 1, "flour": 2, "sugar": 4, "noodles": 4}


def test__cooking_with_unsufficient_ingredients():
    """The ingredients are not substracted, if ingredients not sufficient."""
    inventory = Inventory(milk=2, flour=1, sugar=2, noodles=4)
    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)

    cooking_service = CookingService(inventory)

    with raises(CookingException, match="Not enough ingredients to cook the recipe"):
        cooking_service.cook_recipe(cookies)

    assert inventory == {"milk": 2, "flour": 1, "sugar": 2, "noodles": 4}
