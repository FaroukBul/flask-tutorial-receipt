from sqlalchemy import (
    Column, Integer, String
)
from flaskr.models import db, MyModel


class Customer(db.Model, MyModel): 
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    address = Column(String(150), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    receipts = db.relationship(
        'Receipt',
        backref='author',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def get(id):
        return Customer.query.get(id)

    def get_all():
        return Customer.query.all()
    
    def search(search_term):
        customer = Customer.query.filter_by(name=search_term).first()
        if customer is None:
            customer = Customer.query.filter_by(email=search_term).first()
        if customer is None:
            customer = Customer.query.filter_by(address=search_term).first()
        
        return customer
    
    @property
    def request(self):
        from .request import CustomerRequest
        return CustomerRequest(self)
    


        