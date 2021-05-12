from sqlalchemy import (
    Column, Integer, String, 
    Text, Float, ForeignKey
)
from flaskr.models import db, MyModel, commit_to_db


class Receipt(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    sold_products = db.relationship(
        'SoldProduct',
        backref='receipt',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def search(search_term):
        search_result = Receipt.query.filter_by(name=search_term).first()
        return search_result
    
    def get(id):
        return Receipt.query.get(id)

    def get_all():
        return Receipt.query.all()
    
    @property
    def request(self):
        from .request import ReceiptRequest
        return ReceiptRequest(self)


class SoldProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    


  
