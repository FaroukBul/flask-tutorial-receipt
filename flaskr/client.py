from flask import (
    Blueprint, render_template, request, 
    g, session, flash

)
from flaskr.db import get_db
bp = Blueprint('client', __name__)

@bp.route('/add-client', methods=("GET", "POST"))
def add_client():
    db = get_db()
    fields = ["name", "address", "e_mail", "phone"]
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        e_mail = request.form['e_mail']
        phone = request.form['phone']
        client_name = db.execute('SELECT name FROM client WHERE name = ?',
        (name,)).fetchone()

        if client_name is not None:
            flash("Client name already exists on the database, try a diferent one.")

        if client_name is None: 
            db.execute('INSERT or IGNORE INTO client (name, address, e_mail, phone) VALUES (?, ?, ?, ?)',(
                name, address, e_mail, phone
            ))
            db.commit()

    
    return render_template(
        "client/add-client.html",
        fields=fields
    )

@bp.route('/clients')
def clients():
    db = get_db()
    clients = db.execute('SELECT * FROM client').fetchall()

    return render_template( 
        "client/clients.html", 
        clients=clients
        )


def get_client(id):
    client = get_db().execute(
        'SELECT * FROM client WHERE id = ?',
        (str(id))
    ).fetchone()

    return client

@bp.route('/update-client/<int:id>', methods=("GET", "POST"))
def update_client(id):
    db = get_db()
    fields = ['name', 'address', 'e_mail', 'phone']

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        e_mail = request.form['e_mail']
        phone = request.form['phone']
        client_name = db.execute('SELECT name FROM client WHERE name = ?',
        (name,)).fetchone()
      
        if client_name is not None: 
            flash("Client name already exists on the database, try a diferent one.")
        else:
            db.execute(
                'UPDATE client SET name = ?, address = ?, e_mail = ?, phone = ?'
                'WHERE id = ?',
                (name, address, e_mail, phone, id)
            )
            db.commit()

    client = get_client(id)

    return render_template(
        'client/update-client.html',
        fields=fields,
        client=client
    )







