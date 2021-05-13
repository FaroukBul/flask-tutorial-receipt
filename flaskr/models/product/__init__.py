from sqlalchemy import (
    Column, Integer, String, 
    Text, Float
)
from flaskr.models import db, MyModel


class Product(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text(1000), nullable=False)
    price = Column(Float, nullable=False, default=0)
    sold_products = db.relationship(
        'SoldProduct',
        backref='product',
        lazy=True, 
        cascade='all, delete-orphan'
    )
    
    def search(search_term):
        return Product.query.filter_by(name=search_term).first()
       
    def get(id):
        return Product.query.get(id)
    
    def get_all():
        return Product.query.all()

    @property
    def request(self):
        from .request import ProductRequest
        return ProductRequest(self)


