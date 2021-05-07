from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column, Integer, String
)
import click
from flask.cli import with_appcontext

db = SQLAlchemy()


class Customer(db.Model): 
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    address = Column(String(150), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)


def init_db():
    db.drop_all()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


