"""Unit tests for the Inventory class."""
import shutil
from inventory_app.inventory import InventoryLoader, InventorySerializer, LiveInventory


def test__live_edit_will_persist():
    """A live edit with statement will safe the inventory on exit."""
    shutil.copyfile("tests/persistance/valid.json5", "tests/tmp/live.json5")

    with LiveInventory(InventoryLoader("tests/tmp/live", InventorySerializer())) as inventory:
        inventory.add("milk", 2)
        inventory.remove("sugar", 0.25)

    actual = InventoryLoader("tests/tmp/live", InventorySerializer()).load_inventory()
    expected = InventoryLoader("tests/persistance/live", InventorySerializer()).load_inventory()
    assert actual == expected


def test__live_edit_twice_will_accumulate():
    """A live edit with statement will safe the inventory on exit."""
    shutil.copyfile("tests/persistance/valid.json5", "tests/tmp/accumulated.json5")

    live_inventory = LiveInventory(InventoryLoader("tests/tmp/accumulated", InventorySerializer()))

    with live_inventory as inventory:
        inventory.add("milk", 2)
        inventory.remove("sugar", 0.25)

    with live_inventory as inventory:
        inventory.add("milk", 3)
        inventory.add("cheese")

    actual = InventoryLoader("tests/tmp/accumulated", InventorySerializer()).load_inventory()
    expected = InventoryLoader("tests/persistance/accumulated", InventorySerializer()).load_inventory()
    assert actual == expected
