import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    '''
    Returns a json formatted dictionary representing the store.
    {'name': <itemname>, 'items': <items>}
    '''
    def json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name, 
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

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