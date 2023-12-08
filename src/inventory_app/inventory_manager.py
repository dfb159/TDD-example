"""Main Inventory Manager API."""


class InventoryManager():
    """The Inventory Manager will persist items in its lifetime."""
    inventory: dict[str, float]

    def __init__(self) -> None:
        self.inventory = {}

    def __len__(self):
        return len(self.inventory)

    def __getitem__(self, item: str):
        return self.inventory[item] if item in self.inventory else 0

    def __setitem__(self, item: str, quantity: float):
        if quantity <= 0:
            self.remove(item)
        else:
            self.inventory[item] = quantity

    def __contains__(self, item: str):
        return item in self.inventory

    def add(self, item: str, quantity: float = 1):
        """Adds an item to the inventory."""
        if quantity == 0:
            return

        if quantity < 0:
            self.remove(item, -quantity)
        elif item not in self.inventory:
            self.inventory[item] = quantity
        else:
            self.inventory[item] += quantity

    def remove(self, item: str, quantity: float | None = None):
        """Removes the given item from the inventory."""
        if quantity is not None:
            if quantity < 0:  # nested if: Pylint does not get it otherwise
                self.add(item, -quantity)
                return

        if item not in self.inventory:
            return

        stored = self.inventory[item]
        if quantity is None or stored <= quantity:
            del self.inventory[item]
        else:
            self.inventory[item] -= quantity

    def items(self):
        """List of all items of this inventory."""
        return self.inventory.keys()
