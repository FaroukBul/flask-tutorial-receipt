from flask import (
    Blueprint, render_template, request, 
    redirect, url_for
)

from . import get_form
from flaskr.models.receipt import Receipt
from flaskr.models.customer import Customer
bp = Blueprint('receipt', __name__, url_prefix='/receipt')


receipt_heads = [
    'name',
    'address',
    'email'
]

@bp.route('/receipts')
def receipts():
    receipts = Receipt.get_all()
    
    return render_template(
        'receipt/receipts.html',
        receipts=receipts,
        heads=receipt_heads
    )


@bp.route('/add', methods=('GET', 'POST'))
def add():
    form = get_form(receipt_heads)
    if request.method == 'POST':
        customer = Customer.search(form['name'])
        receipt = Receipt(
            customer_id=customer.id
        )
        receipt.add()
    
    return render_template(
        'receipt/add.html',
        heads=receipt_heads,
        customer=None
    )

@bp.route('/update/<int:receipt_id>', methods=('GET', 'POST'))
def update(receipt_id):
    receipt = Receipt.get(receipt_id)
    
    if request.method == 'POST':
        error = receipt.request.update()
        if not error:
            return redirect(
                url_for('receipt.receipts')
            )

    return render_template(
        'receipt/update.html',
        customer=receipt.author,
        heads=receipt_heads
    )


