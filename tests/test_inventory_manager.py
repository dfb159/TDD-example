from inventory_app.inventory_manager import InventoryManager


def test__init_empty_manager__should_be_empty():
    inventory = InventoryManager()
    assert len(inventory) == 0


def test__add_items__should_be_saved():
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.add("sugar")
    assert len(inventory) == 2
    assert set(inventory.items()) == set(["milk", "sugar"])


def test__add_items_twice__should_add_once():
    inventory = InventoryManager()
    inventory.add("milk")
    inventory.add("milk")
    assert len(inventory) == 1


def test__remove_item_should_work():
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0


def test__remove_item_then_add_should_work():
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    assert len(inventory) == 0


def test__remove_item_twice_should_not_error():
    inventory = InventoryManager()
    inventory.add("milk")
    assert len(inventory) == 1
    inventory.remove("milk")
    inventory.remove("milk")
    assert len(inventory) == 0
