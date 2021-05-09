from flask import request


class CustomerRequest:

    def __init__(self, customer):
        self.customer = customer
        self.heads = [
            'name',
            'address',
            'email'
        ]
        self.repeated_err_msg = "Thats not avaliable"

    def add(self):
        error = self.validate()
        if not error:
            try:
                self.customer.add()
            except ValueError:
                error = self.repeated_err_msg

        return error 

    def update(self):    
        self.customer.name = request.form["name"]
        self.customer.address = request.form["address"]
        self.customer.email = request.form["email"]

        error = self.validate()
        if not error:
            try:
                self.customer.update()
            except ValueError:
                error = self.repeated_err_msg
        
        return error

    def validate(self):
        for head in self.heads:
            value = getattr(self.customer, head)
            if value == "":
                return "There cant be any empty fields"
        
        return None
    
        