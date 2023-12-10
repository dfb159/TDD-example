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


def _fullpath(path: str):
    if not path.endswith((".json", ".json5")):
        path += ".json5"
    return path


def _load_inventory(file: TextIOWrapper) -> dict[str, float]:
    try:
        data = json5.load(file)
    except Exception as e:
        raise InvalidFileFormat() from e

    if not isinstance(data, dict):
        raise InvalidFileFormat("Content is not of type dict")

    return _check_inner_dict(data)


def _check_inner_dict(data: dict) -> dict[str, float]:
    for key, value in data.items():
        if not isinstance(key, str):
            raise InvalidFileFormat(f"Content key '{key}' is not of type str")
        if not isinstance(value, Number):
            raise InvalidFileFormat(f"Content key '{value}' is not a number")
    return data


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

    def __init__(self, path: Optional[str] = None):
        """
        Initialize the Inventory object.

        Arguments:
            path (Optional[str]): The path to the inventory file. If provided, the inventory will be loaded from the file.
        """
        self.inventory = {}
        self.path = path
        if self.path:
            with open(_fullpath(self.path), 'r', encoding="utf-8") as file:
                self.inventory = _load_inventory(file)

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

    def __eq__(self, other: Self):
        return self.inventory == other.inventory

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

    def save(self, path: str):
        """Save the inventory to a file.

        Arguments:
            path (str): The path to save the inventory to.
        """
        fullpath = _fullpath(path)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        with open(fullpath, 'w', encoding="utf-8") as file:
            json5.dump(self.inventory, file)


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

    Methods:
        __init__(self, path: str): Initializes the LiveInventory object with the given path.
        __enter__(self) -> Inventory: Enters the context and returns the inventory manager.
        __exit__(self, exc_type, exc_value, traceback) -> bool: Exits the context and saves the inventory.
    """

    path: str
    manager: Inventory

    def __init__(self, path: str):
        self.path = path

    def __enter__(self) -> Inventory:
        self.manager = Inventory(self.path)
        return self.manager

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        if exc_value is not None:
            return False

        self.manager.save(self.path)
        return True
