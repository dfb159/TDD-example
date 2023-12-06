"""Tests for the basic Inventory API."""
from inventory_app.inventory_manager import InventoryManager


def test__init_empty_manager():
    """A newly instanciated manager should be empty."""
    inventory = InventoryManager()
    assert len(inventory) == 0


def test__add_items():
    """Adding items to the manager should be persisted."""
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.add("sugar")
    assert len(inventory) == 2
    assert set(inventory.items()) == set(["milk", "sugar"])
    assert inventory["milk"] == 1
    assert inventory["sugar"] == 1


def test__add_items_twice():
    """Adding the same item twice should still be added, but not throw an exception."""
    inventory = InventoryManager()
    inventory.add("milk")
    inventory.add("milk")
    assert len(inventory) == 1
    assert inventory["milk"] == 2


def test__add_item_quantity():
    """Add specific quantity will update items."""
    inventory = InventoryManager()
    inventory.add("milk", 3.3)
    assert len(inventory) == 1
    assert inventory["milk"] == 3.3


def test__set_item_quantity():
    """Set specific quantity will update items."""
    inventory = InventoryManager()
    inventory["milk"] = 2.4
    assert len(inventory) == 1
    assert inventory["milk"] == 2.4


def test__remove_item():
    """Removing an item will delete it from the list."""
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0


def test__remove_item_then_add():
    """Adding a removed item should not throw."""
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0


def test__remove_item_twice():
    """Removing an item twice does not throw."""
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    inventory.remove("milk")
    assert len(inventory) == 0
    assert inventory["milk"] == 0


def test__remove_item_quantity():
    """Removing an item with specific quantity."""
    inventory = InventoryManager()
    inventory.add("milk", 4.2)
    assert len(inventory) == 1
    inventory.remove("milk", 1.8)
    assert inventory["milk"] == 2.4
    assert len(inventory) == 1


def test__remove_item_all():
    """Removing complete item."""
    inventory = InventoryManager()
    inventory.add("milk", 4.2)
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0


def test__unknown_item():
    """If the item does not exist, then the amount is zero."""
    inventory = InventoryManager()
    assert inventory["milk"] == 0
