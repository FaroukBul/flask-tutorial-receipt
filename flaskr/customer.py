from flask import (
    Blueprint, render_template, request, url_for, redirect
)
from flaskr.models.customer import Customer
bp = Blueprint("customer", __name__, url_prefix='/customer')


customer_heads = {
    'name': "name",
    'address': 'address',
    'email': 'email'
}

@bp.route('/customers')
def customers():
    customers = Customer.get_all()
    
    return render_template(
        "customer/customers.html",
        customers=customers,
        heads=customer_heads
    )


@bp.route('/add', methods=('GET', 'POST'))
def add():
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
        'customer/add.html',
        customer_heads=customer_heads
    )


@bp.route('/update/<int:customer_id>', methods=('GET', 'POST'))
def update_customer(customer_id):
    customer = Customer.get(customer_id)

    if request.method == 'POST':
        customer.name = request.form["name"]
        customer.address = request.form["address"]
        customer.email = request.form["email"]

        customer.update()

    return render_template(
        'customer/update.html',
        heads=customer_heads, 
        customer=customer
    )


@bp.route('/delete/<int:customer_id>')
def delete(customer_id):
    customer = Customer.get(customer_id)
    customer.delete()

    return redirect(
        url_for('customer.customers')
    )
