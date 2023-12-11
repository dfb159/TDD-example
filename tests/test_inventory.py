"""Unit tests for the Inventory class."""
from pytest import approx
from inventory_app.inventory import Inventory


def test__init_empty_inventory():
    """A newly instanciated inventory should be empty."""
    inventory = Inventory()
    assert len(inventory) == 0
    assert "milk" not in inventory


def test__add_items():
    """Adding items to the inventory should be persisted."""
    inventory = Inventory()
    inventory.add("milk")
    assert "milk" in inventory
    assert "sugar" not in inventory
    assert len(inventory) == 1
    inventory.add("sugar")
    assert "sugar" in inventory
    assert len(inventory) == 2
    assert set(inventory.keys()) == set(["milk", "sugar"])
    assert inventory["milk"] == 1
    assert inventory["sugar"] == 1


def test__add_zero():
    """Adding zero items to the inventory should not add an item."""
    inventory = Inventory()
    inventory.add("milk", 0)
    assert "milk" not in inventory
    assert len(inventory) == 0
    assert inventory["milk"] == 0


def test__add_negative():
    """Adding negative items to the inventory should behave like remove."""
    inventory = Inventory()
    inventory.add("milk", 2)
    assert "milk" in inventory
    inventory.add("milk", -1)
    assert "milk" in inventory
    assert inventory["milk"] == 1
    inventory.add("milk", -1.5)
    assert "milk" not in inventory
    assert inventory["milk"] == 0


def test__set_zero():
    """Set items to zero will do nothing."""
    inventory = Inventory()
    inventory["milk"] = 0
    assert "milk" not in inventory
    assert len(inventory) == 0
    assert inventory["milk"] == 0


def test__add_and_set_zero():
    """Set items to zero after adding will remove the item."""
    inventory = Inventory()
    inventory["milk"] = 2
    assert "milk" in inventory
    inventory["milk"] = 0
    assert "milk" not in inventory


def test__set_negative():
    """Setting item to a negative should set them to zero."""
    inventory = Inventory()
    inventory["milk"] = 0
    assert "milk" not in inventory
    assert len(inventory) == 0
    assert inventory["milk"] == 0


def test__add_items_twice():
    """Adding the same item twice should accumulate them."""
    inventory = Inventory()
    inventory.add("milk")
    inventory.add("milk")
    assert "milk" in inventory
    assert len(inventory) == 1
    assert inventory["milk"] == 2


def test__add_item_quantity():
    """Add specific quantity will update items."""
    inventory = Inventory()
    inventory.add("milk", 3.3)
    assert "milk" in inventory
    assert len(inventory) == 1
    assert inventory["milk"] == approx(3.3)


def test__set_item_quantity():
    """Set specific quantity will replace item quantity."""
    inventory = Inventory()
    inventory["milk"] = 2.4
    assert "milk" in inventory
    assert len(inventory) == 1
    assert inventory["milk"] == approx(2.4)


def test__remove_item():
    """Removing an item will delete it from the list."""
    inventory = Inventory()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0
    assert "milk" not in inventory


def test__remove_item_then_add():
    """Adding a removed item should not throw."""
    inventory = Inventory()
    inventory.add("milk")
    assert len(inventory) == 1
    assert "milk" in inventory
    inventory.remove("milk")
    assert len(inventory) == 0
    assert "milk" not in inventory
    inventory.add("milk")
    assert len(inventory) == 1
    assert "milk" in inventory
    inventory.remove("milk")
    assert len(inventory) == 0
    assert "milk" not in inventory


def test__remove_item_twice():
    """Removing an item twice does not throw."""
    inventory = Inventory()
    inventory.add("milk")
    assert len(inventory) == 1
    assert "milk" in inventory
    inventory.remove("milk")
    inventory.remove("milk")
    assert "milk" not in inventory
    assert len(inventory) == 0
    assert inventory["milk"] == 0


def test__remove_item_quantity():
    """Removing an item with specific quantity."""
    inventory = Inventory()
    inventory.add("milk", 4.2)
    assert "milk" in inventory
    assert len(inventory) == 1
    inventory.remove("milk", 1.8)
    assert "milk" in inventory
    assert len(inventory) == 1
    assert inventory["milk"] == approx(2.4)


def test__remove_negative_item_quantity():
    """Removing negative amouns of items should act like adding."""
    inventory = Inventory()
    inventory.remove("milk", -4.2)
    assert "milk" in inventory
    assert len(inventory) == 1
    assert inventory["milk"] == approx(4.2)
    inventory.remove("milk", -1.8)
    assert "milk" in inventory
    assert len(inventory) == 1
    assert inventory["milk"] == approx(6)


def test__remove_all_item_quantity():
    """Removing all items with huge quantity."""
    inventory = Inventory()
    inventory.add("milk", 4.2)
    assert "milk" in inventory
    assert len(inventory) == 1
    inventory.remove("milk", 7.3)
    assert inventory["milk"] == 0
    assert "milk" not in inventory
    assert len(inventory) == 0


def test__remove_item_all():
    """Removing complete item."""
    inventory = Inventory()
    inventory.add("milk", 4.2)
    assert "milk" in inventory
    assert len(inventory) == 1
    inventory.remove("milk")
    assert "milk" not in inventory
    assert len(inventory) == 0
    assert inventory["milk"] == 0


def test__remove_item_del():
    """Removing an item with del dunder should remove all."""
    inventory = Inventory()
    inventory.add("milk")
    assert len(inventory) == 1
    del inventory["milk"]
    assert len(inventory) == 0
    assert "milk" not in inventory


def test__unknown_item():
    """If the item does not exist, then the amount is zero."""
    inventory = Inventory()
    assert inventory["milk"] == 0
