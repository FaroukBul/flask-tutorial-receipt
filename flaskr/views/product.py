from flask import (
    Blueprint, render_template, request, 
    redirect, url_for
)
from flaskr.models.product import Product
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
    form_add_product = {}
    for key in product_heads:
        form_add_product[key] = ""

    if request.method == "POST":
        for key in form_add_product:
            form_add_product[key] = request.form[key]
        
        product = Product(
            name=form_add_product['name'],
            description=form_add_product['description'],
            price=form_add_product['price'],
        )

        product.add()
    
    return render_template(
        'product/add.html',
        product_heads=product_heads
    )


@bp.route('/update/<int:product_id>', methods=("GET", "POST"))
def update(product_id):
    product = Product.get(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])

        product.update()

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




    
