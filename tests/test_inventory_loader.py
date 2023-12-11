"""Unit tests for the Inventory class."""
import json5
from pytest import approx, raises
from inventory_app.inventory import Inventory, InventoryLoader, InvalidFileFormat


def test__load_from_disk():
    """Loads an existing file in the correct format."""
    loader = InventoryLoader("tests/persistance/valid")
    inventory = loader.load_inventory()
    assert inventory == {"milk": 3, "sugar": approx(1.4), "cheese": 1}


def test__load_wrong_from_disk():
    """Loads an existing file in an invalid format."""
    loader = InventoryLoader("tests/persistance/invalid")
    with raises(InvalidFileFormat, match="Content value 'gupta' for key 'sugar' is not a number"):
        loader.load_inventory()


def test__save_to_disk():
    """Saves an inventory to the disk."""
    inventory = Inventory(milk=3, sugar=1.4, cheese=1)

    loader = InventoryLoader("tests/tmp/save")
    loader.save_inventory(inventory)

    with open("tests/tmp/save.json5", 'r', encoding="utf-8") as f1, open("tests/persistance/valid.json5", 'r', encoding="utf-8") as f2:
        assert json5.load(f1) == json5.load(f2)


def test__disk_roundtrip():
    """Saves and loads an inventory. Check if same."""
    inventory = Inventory(milk=3, sugar=1.4)

    loader = InventoryLoader("tests/tmp/roundtrip")
    loader.save_inventory(inventory)
    loaded_inventory = loader.load_inventory()
    assert inventory == loaded_inventory
