from flask import (
    Blueprint, render_template, request, 
    g, flash
)
from flaskr.db import get_db
bp = Blueprint('product', __name__)

@bp.route("/add-product", methods=("GET", "POST"))
def add_product():
    db = get_db()
    heads = ["name", "price", "description"]
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form['description']
        error = None
        product_name = db.execute(
            'SELECT name FROM product WHERE name = ?', (name,)
        ).fetchone()

        if product_name is not None:
            flash("Product name already exists, try a different one")
        if product_name is None:
            db.execute("INSERT or IGNORE INTO product (name, price, description) VALUES (?, ?, ?)",(
                name, price, description
            ))
            db.commit()
    
    return render_template(
        "product/add-product.html",
        heads=heads
    )


@bp.route("/products")
def products():
    db = get_db()
    products = db.execute("SELECT * FROM product").fetchall()

    return render_template("product/products.html", products=products)




def get_product(id):
    product = get_db().execute(
        'SELECT * FROM product WHERE id = ?',
        (str(id))
    ).fetchone()

    return product


@bp.route("/update-product/<int:id>", methods=("GET", "POST"))
def update_product(id):
    db = get_db()
    product = get_product(id) ## ?????
    heads = ["name", "price", "description"]


    if  not product:
        flash("Product not found") 

    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        error = None
        product_name = db.execute(
            'SELECT name FROM product WHERE name = ?', (name,)
        ).fetchone()

        if product_name is not None:
            flash("Product name already exists, try a different one.")

        if product_name is None:
            db.execute(
                'UPDATE product SET name = ?, price = ?, description = ?'
                'WHERE id = ?',
                (name, price, description, id)
            )
            db.commit()
            product = get_product(id)

    return render_template(
        'product/update-product.html',
        heads=heads,
        product=product
    )







