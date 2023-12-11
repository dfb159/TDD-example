"""Unit tests for the Inventory class."""
from inventory_app.inventory import Inventory


def test__init_empty_inventory():
    """A newly instanciated inventory should be empty."""
    inventory = Inventory()
    assert inventory.__dict__["_Inventory__inventory"] == {}


def test__init_inventory_stored():
    """A newly instanciated inventory should have the given items stored."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory.__dict__["_Inventory__inventory"] == {"milk": 2, "sugar": 1}


def test__get_positive_amount():
    """__get__ dunder for a stored item."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory["milk"] == 2


def test__get_not_existing_amount():
    """__get__ dunder for a missing item."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory["flour"] == 0


def test__set_new_item():
    """__set__ dunder for a not existing item."""
    inventory = Inventory()
    inventory["flour"] = 4
    assert inventory["flour"] == 4


def test__set_new_item_zero():
    """__set__ dunder for a not existing item."""
    inventory = Inventory()
    inventory["flour"] = 0
    assert inventory["flour"] == 0


def test__set_new_item_negative():
    """__set__ dunder for a not existing item."""
    inventory = Inventory()
    inventory["flour"] = -4
    assert inventory["flour"] == 0


def test__set_override_item():
    """__set__ dunder for an already existing item."""
    inventory = Inventory(milk=2, sugar=1)
    inventory["milk"] = 4
    assert inventory["milk"] == 4


def test__set_override_item_zero():
    """__set__ dunder for an already existing item."""
    inventory = Inventory(milk=2, sugar=1)
    inventory["milk"] = 0
    assert inventory["milk"] == 0


def test__set_override_item_negative():
    """__set__ dunder for an already existing item."""
    inventory = Inventory(milk=2, sugar=1)
    inventory["milk"] = -4
    assert inventory["milk"] == 0


def test__set_increment():
    """__set__ and __get__ dunder for += assignment."""
    inventory = Inventory(milk=2, sugar=1)
    inventory["milk"] += 3
    assert inventory["milk"] == 5


def test__del_existing():
    """__del__ dunder removes an item completely."""
    inventory = Inventory(milk=2, sugar=1)
    del inventory["milk"]
    assert inventory["milk"] == 0


def test__del_not_existing():
    """__del__ dunder will not crash on not existing items."""
    inventory = Inventory(milk=2, sugar=1)
    del inventory["flour"]
    assert inventory["flour"] == 0


def test__contains_existing():
    """__contains__ dunder for an existing item."""
    inventory = Inventory(milk=2, sugar=1)
    assert "milk" in inventory


def test__contains_not_existing():
    """__contains__ dunder for a not existing item."""
    inventory = Inventory(milk=2, sugar=1)
    assert "flour" not in inventory


def test__equals_inventories():
    """__equals__ dunder for two equal inventories."""
    inventory1 = Inventory(milk=2, sugar=1)
    inventory2 = Inventory(milk=2, sugar=1)
    assert inventory1 == inventory2


def test__equals_inventories_different_names():
    """__equals__ dunder for two unequal inventories. item name is different."""
    inventory1 = Inventory(milk=2, sugar=1)
    inventory2 = Inventory(milk=2, flour=1)
    assert inventory1 != inventory2
    assert not inventory1 == inventory2


def test__equals_inventories_different_values():
    """__equals__ dunder for two unequal inventories. item value is different."""
    inventory1 = Inventory(milk=2, sugar=1)
    inventory2 = Inventory(milk=2, sugar=2)
    assert inventory1 != inventory2
    assert not inventory1 == inventory2


def test__equals_dictionary():
    """__equals__ dunder for an inventory equal to its respective item dict."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory == {"milk": 2, "sugar": 1}


def test__equals_dictionary_different_keys():
    """__equals__ dunder for an inventory equal to its respective item dict."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory != {"milk": 2, "flour": 1}


def test__equals_dictionary_different_values():
    """__equals__ dunder for an inventory equal to its respective item dict."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory != {"milk": 2, "sugar": 2}


def test__add_items():
    """Adding items to the inventory should be persisted."""
    inventory = Inventory()
    inventory.add("milk")
    assert inventory["milk"] == 1


def test__add_items_twice():
    """Adding the same item twice should accumulate them."""
    inventory = Inventory()
    inventory.add("milk")
    inventory.add("milk")
    assert inventory["milk"] == 2


def test__add_item_quantity():
    """Add specific quantity will update items."""
    inventory = Inventory()
    inventory.add("milk", 5)
    assert inventory["milk"] == 5


def test__add_zero():
    """Adding zero items to the inventory should not add an item."""
    inventory = Inventory()
    inventory.add("milk", 0)
    assert "milk" not in inventory


def test__add_negative():
    """Adding negative items to the inventory should remove them."""
    inventory = Inventory(milk=2)
    inventory.add("milk", -1)
    assert inventory["milk"] == 1


def test__add_many_negative():
    """Adding too many negative items to the inventory should set to zero."""
    inventory = Inventory(milk=2)
    inventory.add("milk", -3)
    assert "milk" not in inventory


def test__remove_item():
    """Removing an item will delete it from the list."""
    inventory = Inventory(milk=3)
    inventory.remove("milk")
    assert "milk" not in inventory


def test__remove_item_quantity():
    """Removing an item will delete the given quantity from the list."""
    inventory = Inventory(milk=3)
    inventory.remove("milk", 2)
    assert inventory["milk"] == 1


def test__remove_item_many_quantity():
    """Removing many items will remove it from the list."""
    inventory = Inventory(milk=3)
    inventory.remove("milk", 4)
    assert "milk" not in inventory


def test__remove_negative_item_quantity():
    """Removing negative amouns of items should act like adding."""
    inventory = Inventory(milk=2)
    inventory.remove("milk", -3)
    assert inventory["milk"] == 5


def test__remove_item_then_add():
    """Adding a removed item should not throw."""
    inventory = Inventory(milk=1)
    assert "milk" in inventory
    inventory.remove("milk")
    assert "milk" not in inventory
    inventory.add("milk")
    assert "milk" in inventory
    inventory.remove("milk")
    assert "milk" not in inventory


def test__remove_item_twice():
    """Removing an item twice does not throw."""
    inventory = Inventory(milk=2)
    inventory.remove("milk")
    inventory.remove("milk")
    assert "milk" not in inventory


def test__items_should_be_like_inner_items():
    """The items of an inventory should be like the inner items."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory.items() == {("milk", 2), ("sugar", 1)}


def test__names_should_be_like_inner_names():
    """The names of an inventory should be like the inner names."""
    inventory = Inventory(milk=2, sugar=1)
    assert inventory.names() == {"milk", "sugar"}
