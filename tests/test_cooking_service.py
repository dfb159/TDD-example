"""Unit tests for the CookingService class."""

from pytest import raises
from inventory_app.inventory import Inventory
from inventory_app.recipe import Recipe
from inventory_app.cooking_service import CookingException, CookingService


def test__recipe_ingredients_availiable():
    """The ingredients of a recipe are availiable in the inventory."""
    inventory = Inventory()
    inventory.add("milk", 5)
    inventory.add("flour", 3)
    inventory.add("sugar", 2)
    inventory.add("noodles", 4)

    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)

    cooking_service = CookingService()
    assert cooking_service.is_cookable(cookies, inventory)


def test__recipe_scaled_ingredients_availiable():
    """The ingredients of a recipe are availiable even after scaling in the inventory."""
    inventory = Inventory()
    inventory.add("milk", 5)
    inventory.add("flour", 7)
    inventory.add("sugar", 3)
    inventory.add("noodles", 4)

    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)
    more_cookies = cookies.for_portions(4)

    cooking_service = CookingService()
    assert cooking_service.is_cookable(more_cookies, inventory)


def test__recipe_ingredients_not_enough():
    """The ingredients of a recipe are not availiable in the inventory."""
    inventory = Inventory()
    inventory.add("milk", 5)
    inventory.add("flour", 3)
    inventory.add("sugar", 2)
    inventory.add("noodles", 4)

    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=4)

    cooking_service = CookingService()
    assert not cooking_service.is_cookable(cookies, inventory)


def test__recipe_scaling_ingredients_not_enough():
    """The ingredients of a recipe are only not availiable after scaling."""
    inventory = Inventory()
    inventory.add("milk", 2)
    inventory.add("flour", 3)
    inventory.add("sugar", 2)
    inventory.add("noodles", 4)

    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)
    more_cookies = cookies.for_portions(4)

    cooking_service = CookingService()
    assert not cooking_service.is_cookable(more_cookies, inventory)


def test__cooking_a_recipe():
    """The ingredients are substracted on cooking."""
    inventory = Inventory()
    inventory.add("milk", 2)
    inventory.add("flour", 4)
    inventory.add("sugar", 5)
    inventory.add("noodles", 4)

    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)

    cooking_service = CookingService()
    cooking_service.cook_recipe(cookies, inventory)

    assert inventory["milk"] == 1
    assert inventory["flour"] == 2
    assert inventory["sugar"] == 4
    assert inventory["noodles"] == 4


def test__cooking_a_scaled_recipe():
    """The ingredients are not substracted, if ingredients not sufficient."""
    inventory = Inventory()
    inventory.add("milk", 2)
    inventory.add("flour", 1)
    inventory.add("sugar", 2)
    inventory.add("noodles", 4)

    cookies = Recipe(portions=2, time=30, milk=1, flour=2, sugar=1)

    cooking_service = CookingService()

    with raises(CookingException, match="Not enough ingredients to cook the recipe"):
        cooking_service.cook_recipe(cookies, inventory)

    assert inventory["milk"] == 2
    assert inventory["flour"] == 1
    assert inventory["sugar"] == 2
    assert inventory["noodles"] == 4
