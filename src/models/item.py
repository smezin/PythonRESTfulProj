import sqlite3
from models.item import ItemModel

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}
    
    @classmethod
    def find_by_name(cls, name):
        pass

    def insert(self):
        pass

    def update(self):
        pass
