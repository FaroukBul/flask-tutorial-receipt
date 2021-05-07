from flask import (
    Blueprint, render_template, request
)
from flaskr.models import Customer
bp = Blueprint("customer", __name__)


customer_heads = {
    'name': "name",
    'address': 'address',
    'email': 'email'
}

@bp.route('/')
def customers():
    customers = Customer.query.all()
    
    return render_template(
        "customer/customers.html",
        customers=customers,
        heads=customer_heads
    )


@bp.route('/add-customer', methods=('GET', 'POST'))
def add_customer():
    form_add_customer ={}
    for key in customer_heads:
        form_add_customer[key] = ""
    
    if request.method == "POST":
        for key in form_add_customer:
            form_add_customer[key] = request.form[key]

        customer = Customer(
            name=form_add_customer["name"],
            address=form_add_customer["address"],
            email=form_add_customer['email']
        )
        customer.add()

    return render_template(
        'customer/add-customer.html',
        customer_heads=customer_heads
    )



