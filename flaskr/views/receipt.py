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
    'price'
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
    error = "Product already selected"
    product = None
    receipt = Receipt.get(receipt_id)
    sold_products = SoldProduct.search_receipt(receipt_id)
    if request.method == 'POST':
        form = get_form(product_input)
        product = Product.search(form['name'])
        for sold in sold_products:
            if sold.product.id == product.id:
                flash(error)
                return redirect(
                    url_for('receipt.update', receipt_id=receipt.id)
                )
        sold_product = SoldProduct(product_id=product.id, receipt_id=receipt.id)
        sold_product.add()
        sold_products = SoldProduct.search_receipt(receipt_id)
        print(sold_products)
    
    return render_template(
        'receipt/update.html',
        product=product,
        customer=None,
        receipt=receipt,
        heads=receipt_customer_heads,
        product_heads=product_heads,
        sold_products=sold_products
    )


@bp.route('/delete/<int:receipt_id>/<int:product_id>', methods=("GET", "POST"))
def delete_product(receipt_id ,product_id):
    
    SoldProduct.delete_product(receipt_id, product_id)

    return redirect(url_for('receipt.update', receipt_id=receipt_id))

@bp.route('/delete/<int:receipt_id>', methods=("GET", "POST"))
def delete_receipt(receipt_id):
    receipt = Receipt.get(receipt_id)
    receipt.delete()

    return redirect(url_for('receipt.receipts', receipt_id=receipt_id))

