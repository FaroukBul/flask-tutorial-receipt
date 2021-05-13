from flask import request
from flaskr.models.customer import Customer
from . import SoldProduct

class ReceiptRequest:

    def __init__(self, receipt):
        self.receipt = receipt
        self.customer = receipt.author
        self.heads = [
            'name',
            'address',
            'email'
        ]
        self.msg = "There can't be any empty fields"
    
    def update(self):
        error = self.validate()
        if error is None:
            self.update_customer()

        return error
        
    def update_customer(self):
        self.customer.update()
        
    def validate(self):
        self.customer.request.update_attributes()
        error = self.customer.request.validate()
        
        return error

    


