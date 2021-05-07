from sqlalchemy import (
    Column, Integer, String
)
from . import db


class Customer(db.Model): 
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    address = Column(String(150), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    def add(self):
        db.session.add(self)
        commit_to_db()
    
    def update(self):
        commit_to_db()
    
    def delete(self):
        db.session.delete(self)
        commit_to_db()

    def get(id):
        return Customer.query.get(id)

    def get_all():
        return Customer.query.all()
    
    def search(search_term):
        customer = Customer.query.filter_by(name=search_term)
        if customer is None:
            customer = Customer.query.filter_by(email=search_term)
        if customer is None:
            customer = Customer.query.filter_by(address=search_term)
        
        return customer
    


        