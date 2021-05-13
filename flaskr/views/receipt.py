from flask import (
    Blueprint, render_template, request, 
    redirect, url_for, flash
)

from . import get_form
from flaskr.models.receipt import Receipt, SoldProduct
from flaskr.models.customer import Customer
from flaskr.models.product import Product

bp = Blueprint('receipt', __name__, url_prefix='/receipt')


receipt_customer_heads = [
    'name',
    'address',
    'email'
]

product_heads = [
    'name',
    'description',
    'address'
]

product_input = ['name']


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
            return redirect(
                url_for('receipt.update', receipt_id=receipt.id )
               )

    return render_template(
        'receipt/add.html',
        receipt=receipt,
        heads=receipt_customer_heads,
        product_heads=product_heads
    )


@bp.route('/update/<int:receipt_id>', methods=('GET', 'POST'))
def update(receipt_id):
    product = None
    receipt = Receipt.get(receipt_id)
    form = get_form(product_input)
    if request.method == 'POST':
        
        product = Product.search(form['name'])
        sold_product = SoldProduct(product_id=product.id, receipt_id=receipt.id)
        sold_product.add()
        receipt.receipt = sold_product
        receipt.update()
        print(receipt.receipt)

        
        
    return render_template(
        'receipt/update.html',
        product=product,
        customer=None,
        receipt=receipt,
        heads=receipt_customer_heads,
        product_heads=product_heads
    )


