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
    'price',
    'total'
]

product_input = [
    'name',
    'quantity',
    'id_product'
    ]
quantity_input = ['quantity']


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
    error_blank = "Cant submit empty fields"
    product = None
    receipt = Receipt.get(receipt_id)
    sold_products = SoldProduct.search_receipt(receipt_id)
    if request.method == 'POST':
        form = get_form(product_input)
        product = Product.search(form['name'])
        if product:
            for sold in sold_products:
                if sold.product.id == product.id:
                    flash(error)
                    return redirect(
                        url_for('receipt.update', receipt_id=receipt.id)
                    )
            sold_product = SoldProduct(product_id=product.id, receipt_id=receipt.id)
            sold_product.quantity = 1
            sold_product.total = product.price
            sold_product.add()
            sold_products = SoldProduct.search_receipt(receipt_id)
        else:
            if form['name'] == 'Product':
                flash(error_blank)
                return redirect(
                            url_for('receipt.update', receipt_id=receipt.id)
                        )
            else:
                add_quantity(form['quantity'], form['id_product'])
                sold_products = SoldProduct.search_receipt(receipt_id)
    receipt_total = get_receipt_total(receipt_id)

    
    return render_template(
        'receipt/update.html',
        product=product,
        customer=None,
        receipt=receipt,
        heads=receipt_customer_heads,
        product_heads=product_heads,
        sold_products=sold_products, 
        receipt_total=receipt_total
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


def add_quantity(quantity ,sold_product_id):
    product = SoldProduct.get(sold_product_id)
    product.quantity = quantity
    product_price = product.product.price
    product.total = product_price * int(quantity)
    product.update()


def get_receipt_total(receipt_id):
    receipts = SoldProduct.search_receipt(receipt_id)
    total = 0
    for receipt in receipts:
        total += receipt.total

    return total


