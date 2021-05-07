from flask import (
    Blueprint, render_template
)
from flaskr.models import Customer, db
bp = Blueprint("customer", __name__)

@bp.route('/')
def customers():
    customer = Customer.query.filter_by(name="fer").first()
    
    return render_template(
        "customer/customers.html",
        customer=customer
    )

    