from flask import Blueprint, render_template, session
from flask_login import login_required

# Estrutura da rota da página inicial
agendamento_route = Blueprint('agendamento', __name__)

@agendamento_route.route('/agendamento')
@login_required
def agendamento():
    link_agenda = "barbearia-overclock-aihkmo"
    nome_usuario = session.get("usuario_nome")
    email_usuario = session.get("usuario_email")
    
    return render_template(
        'agendamento.html', 
        link_cal=link_agenda,
        nome=nome_usuario,
        email=email_usuario
    )