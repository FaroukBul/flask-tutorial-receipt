from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import click
from flask.cli import with_appcontext

db = SQLAlchemy()


def commit_to_db():
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError from None


def init_db():
    db.drop_all()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


