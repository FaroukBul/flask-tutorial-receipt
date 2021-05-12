from flask import (
    Blueprint, render_template, request, 
    redirect, url_for, flash
)

from . import get_form
from flaskr.models.receipt import Receipt
from flaskr.models.customer import Customer
bp = Blueprint('receipt', __name__, url_prefix='/receipt')


receipt_customer_heads = [
    'name',
    'address',
    'email'
]

product_heads = [
    'name',
    'description',
    'price'
]

@bp.route('/receipts')
def receipts():
    receipts = Receipt.get_all()
    
    return render_template(
        'receipt/receipts.html',
        receipts=receipts,
        heads=receipt_customer_heads,
    )


@bp.route('/add', methods=('GET', 'POST'))
def add():
    receipt = None
    form = get_form(receipt_customer_heads)
    if request.method == 'POST':
        customer = Customer.search(form['name'])
        if customer:
            receipt = Receipt(
                customer_id=customer.id
            )
            receipt.add()

    if receipt is not None:
        return render_template(
            'receipt/add.html',
            heads=receipt_customer_heads,
            product_heads=product_heads,
            receipt=receipt,
            customer=None
        )
        
    return render_template(
            'receipt/add.html',
            heads=receipt_customer_heads,
            product_heads=product_heads,
            receipt=receipt,
            customer=None
        )
    

@bp.route('/update/<int:receipt_id>', methods=('GET', 'POST'))
def update(receipt_id):
    receipt = Receipt.get(receipt_id)
    
    if request.method == 'POST':
        error = receipt.request.update()
        if error:
            flash(error)
            
    return render_template(
        'receipt/update.html',
        customer=receipt.author,
        receipt=receipt,
        heads=receipt_customer_heads
    )


