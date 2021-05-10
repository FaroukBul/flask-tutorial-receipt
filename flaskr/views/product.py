from flask import (
    Blueprint, render_template, request, 
    redirect, url_for, flash
)
from flaskr.models.product import Product 
from . import get_form
bp = Blueprint('product', __name__, url_prefix='/product')


product_heads = {
    'name': 'name',
    'description': 'description',
    'price': 'price',
}


@bp.route('/products')
def products():
    products = Product.get_all()

    return render_template(
        'product/products.html',
        products=products,
        heads=product_heads
    )


@bp.route('/add', methods=("GET", "POST"))
def add():
    form = get_form(product_heads)
    if request.method == "POST":
        product = Product(
            name=form["name"],
            description=form["description"],
            price=form['price']
        )
        error = product.request.add()
        if not error: 
            return redirect(
                url_for('product.products')
            )
        flash(error)

    return render_template(
        'product/add.html',
        product_heads=product_heads
    )


@bp.route('/update/<int:product_id>', methods=("GET", "POST"))
def update(product_id):
    product = Product.get(product_id)
    if request.method == 'POST':
        error = product.request.update()
        if not error:
            return redirect(
                url_for('product.products')
            )

        flash(error)

    return render_template(
        'product/update.html',
        product=product, 
        heads=product_heads
    )


@bp.route('/delete/<int:product_id>', methods=("GET", "POST"))
def delete(product_id):
    product = Product.get(product_id)
    product.delete()

    return redirect(url_for('product.products'))




    
