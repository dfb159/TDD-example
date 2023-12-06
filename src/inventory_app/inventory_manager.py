"""Main Inventory Manager API."""


class InventoryManager():
    """The Inventory Manager will persist items in its lifetime."""
    inventory: list[str]

    def __init__(self) -> None:
        self.inventory = []

    def __len__(self):
        return len(self.inventory)

    def add(self, item: str):
        """Adds an item to the inventory."""
        if item not in self.inventory:
            self.inventory.append(item)

    def remove(self, item: str):
        """Removes the given item from the inventory."""
        if item in self.inventory:
            self.inventory.remove(item)

    def items(self):
        """List of all items of this inventory."""
        return self.inventory


# if __name__=="__main__":
#     i = InventoryManager()
#     i.add(1)
