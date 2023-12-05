
class InventoryManager():
    inventory:list[str]
    
    def __init__(self) -> None:
        self.inventory = []
    def __len__(self):
        return len(self.inventory)

    def add(self,item:str):
        if self.inventory.count(item) == 0:
            self.inventory.append(item)
    def items(self):
        return self.inventory
            


# if __name__=="__main__":
#     i = InventoryManager()
#     i.add(1)