from flask import (
    Blueprint, render_template, g,
    flash, request, redirect
)

from flaskr.db import get_db
import json, os

bp = Blueprint('receipt', __name__)


@bp.route("/receipt", methods=("GET", "POST"))
def receipt():
    db = get_db()
    quantity = 1
    total = 0
    fields = ['description',
    'brand', 'image', 'price_unit',
    'price_iva', 'total']
    product = None

    if request.method == "POST":
        name = request.form['name']
        quantity = request.form['quantity']
        product_data = db.execute(
            'SELECT * FROM product WHERE name = ?',
            (name,)
        ).fetchone()

        total = product_data['price'] * int(quantity)
        product = {
            'name': product_data['name'],
            'price': product_data['price'],
            'description': product_data['description'],
            'total': total
        }
        total = product_data['price'] * int(quantity)

    client = get_client()
    

    products = product_budget_list(product)
    return render_template(
        "receipt/receipt.html",
        products=products,
        fields=fields,
        client=client
    )


def product_budget_list(product):
    
    products_list =  [
        {
            'name': '',
            'description': '',
            'price': ''
        },
    ]
    
    if product is not None:
       save_products(product)
       products_list = get_products()

    return products_list


def save_products(product):
    products = get_products()
    products.insert(0, product)
    # current_id = get_receipt_id()  works when the json is not a dictionary. 
    products_record = get_all_receipts_products()
    products_record = products
    # products_record[current_id] = products

    with open('product_record.json', 'w') as products_file:
        json.dump(products_record, products_file)


def get_products():
    with open('product_record.json') as products_file:
        receipts_products = json.load(products_file)

    current_id = get_receipt_id()
    products = receipts_products

    return products


def get_all_receipts_products():
    with open('product_record.json') as products_file:
        receipts_products = json.load(products_file)
    
    return receipts_products


@bp.route('/erase-receipt')
def erase_receipt():
    current_id = get_receipt_id()

    if current_id > 0:
        new_id = current_id - 1
    else:
        new_id = 0

    products_list =  [ 
        {
            'name': '',
            'description': '',
            'price': ''
        },
        ]
    
    client = {
            'name': '',
            'address': '',
            'phone': ''
        }
    with open('product_record.json', 'w') as products_file:
        json.dump(products_list, products_file)
    
    save_client(client)

    receipts_ids = get_all_receipts_id()
    if current_id > 0:
        receipts_ids.remove(current_id)
    dump_to_ids(receipts_ids)
    
    return redirect("receipt")

 
@bp.route('/generate-id')       
def generate_id():
    all_ids = get_all_receipts_id()

    if len(all_ids) == 0:
        start_id_list()
    else:
        all_ids = get_all_receipts_id()
        new_id = all_ids[0] + 1
        all_ids.insert(0, new_id)
        dump_to_ids(all_ids)
    client = {
            'name': '',
            'address': '',
            'phone': ''
        }
    save_client(client)
    return redirect("receipt")


def start_id_list():
    id_list = [0]
    dump_to_ids(id_list)


def get_all_receipts_id():
    with open('receipts_id.json') as receipts_id_file:
        receipts_id = json.load(receipts_id_file)
    
    
    return receipts_id


def get_receipt_id():
    receipts_id = get_all_receipts_id()
    if len(receipts_id) > 0:
        current_id = receipts_id[0]
    else:
        current_id = 0
    
    
    return current_id


def dump_to_ids(item):
    with open('receipts_id.json', 'w') as receipts_id_file:
            json.dump(item, receipts_id_file)


@bp.route('/client-receipt', methods=("GET", "POST"))
def client_receipt():
    db = get_db()
    client = get_client()
    
    if client['name'] == '':
        if request.method == "POST":
            name = request.form["client-name"]
            client = db.execute(
                'SELECT * FROM client WHERE name = ?',
                (name,)
            ).fetchone()
            save_client(client)

    return redirect("receipt")


def save_client(client):
    client_info = {
        'name': client['name'],
        'address': client['address'],
        'phone': client['phone']
    }

    with open('client_record.json', 'w') as client_file:
        json.dump(client_info, client_file)


def get_client():
    with open('client_record.json') as client_file:
        client = json.load(client_file)
    if not client:
        client == None
    
    return client

    

    