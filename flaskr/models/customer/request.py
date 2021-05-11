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
        error =  self.check_for_empty_values()
        if not error:
            error = self.validate_name()
        if not error:
            error = self.validate_email()

        return error

    def check_for_empty_values(self):
        for head in self.heads:
            value = getattr(self.customer, head)
            if value == "":
                return "There cant be any empty fields"
        
        return None

    def validate_name(self):
        nums = "0123456789"
        name = self.customer.name
        for num in nums:
            if num in name:
                return "Name cannot contain numbers"
        
        return None

    def validate_email(self):
        error = None
        if "@" not in self.customer.email:
            error = "Invalid email"
        
        return error



    
        