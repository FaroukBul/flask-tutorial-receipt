from sqlalchemy import (
    Column, Integer, String, 
    Text, Float
)
from . import db, commit_to_db


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text(1000), nullable=False)
    price = Column(Float, nullable=False, default=0)

    def add(self):
        db.session.add(self)
        commit_to_db()

    def update(self):
        commit_to_db()
    
    def delete(self):
        db.session.delete(self)
        commit_to_db()
    
    def search(search_term):
       return Product.query.filter_by(name=search_term)
       
    def get(id):
        return Product.query.get(id)
    
    def get_all():
        return Product.query.all()

    