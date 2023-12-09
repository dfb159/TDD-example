"""Main Inventory API."""


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


class Inventory():
    """The Inventory will persist items in its lifetime."""

    inventory: dict[str, float]
    path: str | None

    def __init__(self, path: Optional[str] = None) -> None:
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
        """Adds an item to the inventory."""

        if quantity == 0:
            return

        if quantity < 0:
            self.remove(item, -quantity)
        elif item not in self.inventory:
            self.inventory[item] = quantity
        else:
            self.inventory[item] += quantity

    def remove(self, item: str, quantity: Optional[float] = None):
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

        return set(self.inventory.keys())

    def save(self, path: str):
        """Save the content of this inventory into a file."""

        fullpath = _fullpath(path)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        with open(fullpath, 'w', encoding="utf-8") as file:
            json5.dump(self.inventory, file)


class LiveInventory:
    """A live representation of a file.
    If opened, the file content is availiable as an Inventory."""

    path: str
    manager: Inventory

    def __init__(self, path: str):
        self.path = path

    def __enter__(self) -> Inventory:
        self.manager = Inventory(self.path)
        return self.manager

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        if exc_value is not None:
            return False

        self.manager.save(self.path)
        return True
