from flask import request
from flaskr.models.customer import Customer


class ReceiptRequest:

    def __init__(self):
        self.customer = Customer.get(self.customer_id)
        self.receipt = receipt
        self.heads = [
            'name',
            'address',
            'email'
        ]
        self.msg = "There can't be any empty fields"
    
    def add(self):
        error = self.validate()
        if error is None:
            try:
                self.receipt.add()
            except ValueError:
                return "Cant save, check for empty fields"
    
    def update(self):
        self.customer.name = request.form["name"]
        self.customer.address = request.form['address']
        self.customer.email = request.form['email']

        error = self.validate()
        if error is None: 
            try:
                self.receipt.update()
            except ValueError:
                return self.msg
    
    def validate(self):
        for head in self.heads:
            value = getattr(self.customer, head)
            if value == "":
                return self.msg
        
        return None
