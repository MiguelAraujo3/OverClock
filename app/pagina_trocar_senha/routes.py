from flask import Blueprint, render_template, request
from flask_login import login_required

alterar_senha_route = Blueprint('alterar_senha', __name__)

@alterar_senha_route.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    return render_template('alterar_senha.html')
