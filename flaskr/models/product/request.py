from flask import request


class ProductRequest:

    def __init__(self, product):
        self.product = product
        self.heads = {
                'name': 'name',
                'description': 'description',
                'price': 'price',
            }
        
    def add(self):
        error = self.validate()
        if not error:
            try:
                self.product.add()
            except ValueError:
                return "That's not available"
        return error
    
    def update(self):
        self.product.name = request.form['name']
        self.product.description = request.form['description']
        self.product.price = request.form['price']

        error = self.validate()
        if not error:
            try:
                self.product.update()
            except ValueError:
                error =  "Product name already in database"

        return error

    def validate(self):
        for head in self.heads: 
            value = getattr(self.product, head)
            if value == "":
                return "There can't be any empty fields"
        
        return None
    
    



