from flask import (
    Blueprint, render_template, request, 
    redirect, url_for
)

bp = Blueprint('receipt', __name__, url_prefix='/receipt')


@bp.route('/receipt')
def receipt():
    return render_template(
        'receipt/receipt.html',
    )