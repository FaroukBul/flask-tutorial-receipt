from flask import (
    Blueprint, render_template, request, url_for, 
    redirect, flash
)
from flaskr.models.customer import Customer
from . import get_form
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
    form = get_form(request, customer_heads)
    if request.method == "POST":
        customer = Customer(
            name=form["name"],
            address=form["address"],
            email=form['email']
        )
        error = customer.request.add()
        if not error:
            return redirect(
                url_for('customer.customers')
            )
        flash(error)

    return render_template(
        'customer/add.html',
        customer_heads=customer_heads,
        form=form
    )



@bp.route('/update/<int:customer_id>', methods=('GET', 'POST'))
def update(customer_id):
    customer = Customer.get(customer_id)

    if request.method == 'POST':
        error = customer.request.update()
        if not error:
            return redirect(
                url_for('customer.customers')
            )
        flash(error)

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
