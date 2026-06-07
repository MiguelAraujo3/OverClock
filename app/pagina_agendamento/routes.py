from flask import Blueprint, render_template
from flask_login import login_required

#Estrutura da rota da página inicial
agendamento_route = Blueprint('agendamento', __name__)

@agendamento_route.route('/agendamento')
@login_required
def agendamento():
    return render_template('agendamento.html')