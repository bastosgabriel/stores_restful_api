import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    '''
    Returns a json formatted dictionary representing the item.
    {'name': <itemname>, 'price': <itemprice>}
    '''
    def json(self) -> dict:
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    '''
    Update or insert item model to .db file.
    '''
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    '''
    Delete item model to .db file.
    '''
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()