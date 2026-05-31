from flask import Blueprint, render_template

#Estrutura da rota da página inicial
agendamento_route = Blueprint('agendamento', __name__)

@agendamento_route.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')