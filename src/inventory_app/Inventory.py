"""
Inventory API.

This module provides classes for managing an inventory of items.

Classes:
    - InvalidFileFormat: An error that occurs when opening a file as an inventory.
    - Inventory: The main inventory class that persists items.
    - LiveInventory: A live representation of a file that can be opened as an inventory.
"""

from io import TextIOWrapper
from numbers import Number
import os
from types import TracebackType
from typing import Optional, Self, Type
import json5


class InvalidFileFormat(Exception):
    """An error occoured during opening a file as an inventory."""


class Inventory:
    """
    Represents an inventory of items.

    This class provides methods for managing an inventory of items, including adding, removing, and saving items.

    Attributes:
        inventory (dict[str, float]): The dictionary representing the inventory, where the keys are item names and the values are quantities.
        path (str | None): The path to the inventory file, if it exists.

    Methods:
        add(self, item: str, quantity: float = 1): Adds a quantity of an item to the inventory.
        remove(self, item: str, quantity: Optional[float] = None): Removes a quantity of an item from the inventory.
        items(self): Returns an iterator over the items in the inventory.
        keys(self): Returns an iterator over names of items in the inventory.
        save(self, path: str): Saves the inventory to a file.
    """

    inventory: dict[str, float]
    """The dictionary representing the inventory, where the keys are item names and the values are quantities."""

    path: str | None
    """The path to the inventory file, if it exists."""

    def __init__(self, **items: float):
        """
        Initialize the Inventory object.

        Arguments:
            **items (float): The items to initialize the inventory with.
        """
        self.inventory = items

    def __len__(self):
        return len(self.inventory)

    def __getitem__(self, item: str):
        return self.inventory[item] if item in self.inventory else 0

    def __setitem__(self, item: str, quantity: float):
        if quantity <= 0:
            self.remove(item)
        else:
            self.inventory[item] = quantity

    def __delitem__(self, item: str):
        del self.inventory[item]

    def __contains__(self, item: str):
        return item in self.inventory

    def __eq__(self, other: Self | dict[str, float]):
        if isinstance(other, dict):
            return self.inventory == other
        elif isinstance(other, Inventory):
            return self.inventory == other.inventory
        else:
            return NotImplemented

    def add(self, item: str, quantity: float = 1):
        """Add the given quantity of an item to the inventory.

        Arguments:
            item (str): The name of the item to add.
            quantity (float, optional): The quantity of the item to add. Defaults to 1.
        """
        if quantity == 0:
            return

        if quantity < 0:
            self.remove(item, -quantity)
        elif item not in self.inventory:
            self.inventory[item] = quantity
        else:
            self.inventory[item] += quantity

    def remove(self, item: str, quantity: Optional[float] = None):
        """Remove the given quantity of an item from the inventory.

        If the quantity is not given or negative, the item is removed completely.

        Arguments:
            item (str): The name of the item to remove.
            quantity (float, optional): The quantity of the item to remove. Defaults to None.
        """
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
        """Return an iterator over the items in the inventory."""
        return self.inventory.items()

    def keys(self):
        """Return an iterator over the keys in the inventory."""
        return self.inventory.keys()


class InventoryLoader:
    """
    A class for loading an inventory from a file.

    This class provides a method for loading an inventory from a file and returning
    an `Inventory` object.
    """

    __path: str
    """The path to the inventory file."""

    def __init__(self, path: str):
        """
        Initialize the InventoryLoader.

        Arguments:
            path (str): The path to the inventory file.
        """
        self.__path = InventoryLoader._fullpath(path)

    def load_inventory(self) -> Inventory:
        """
        Load the inventory from the file and return an Inventory object.

        Returns:
            Inventory: The loaded inventory.
        """
        try:
            with open(self.__path, 'r', encoding="utf-8") as file:
                inventory = InventoryLoader._load_inventory(file)
                return Inventory(**inventory)
        except FileNotFoundError:
            return Inventory()

    def save_inventory(self, inventory: Inventory):
        """Save the inventory to a file.

        Arguments:
            inventory (Inventory): The inventory to save.
        """
        os.makedirs(os.path.dirname(self.__path), exist_ok=True)
        with open(self.__path, 'w', encoding="utf-8") as file:
            json5.dump(inventory, file)

    @staticmethod
    def _fullpath(path: str):
        if not path.endswith((".json", ".json5")):
            path += ".json5"
        return path

    @staticmethod
    def _load_inventory(file: TextIOWrapper) -> dict[str, float]:
        try:
            data = json5.load(file)
        except Exception as e:
            raise InvalidFileFormat(f"File '{file.path}' could not be loaded as json5") from e

        if not isinstance(data, dict):
            raise InvalidFileFormat("Content is not of type dict")

        return InventoryLoader._check_inner_dict(data)

    @staticmethod
    def _check_inner_dict(data: dict[str, float]) -> dict[str, float]:
        for key, value in data.items():
            if not isinstance(key, str):
                raise InvalidFileFormat(f"Content key '{key}' is not of type str")
            if not isinstance(value, Number):
                raise InvalidFileFormat(f"Content value '{value}' for key '{key}' is not a number")
        return data


class LiveInventory:
    """
    A context manager for managing live inventory.

    This class provides a context manager interface for managing live inventory.
    It initializes an `Inventory` object from the given path and returns it when
    entering the context. It also saves the inventory when exiting the context,
    unless an exception occurred.

    Attributes:
        path (str): The path to the inventory file.
        manager (Inventory): The inventory manager.
    """

    __loader: InventoryLoader
    """The inventory loader to use."""

    __inventory: Inventory
    """The inventory of this context manager."""

    def __init__(self, loader: InventoryLoader):
        """
        Initialize an instance of the LiveInventory class.

        Arguments:
            loader (InventoryLoader): The inventory loader to use.
        """
        self.__loader = loader

    def __enter__(self) -> Inventory:
        self.__inventory = self.__loader.load_inventory()
        return self.__inventory

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        if exc_value is not None:
            return False

        self.__loader.save_inventory(self.__inventory)
        return True
