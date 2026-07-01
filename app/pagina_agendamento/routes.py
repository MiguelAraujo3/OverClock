from flask import Blueprint, flash, render_template, session, url_for, redirect
from flask_login import login_required

# Estrutura da rota da página inicial
agendamento_route = Blueprint('agendamento', __name__)

@agendamento_route.route('/agendamento')
@login_required
def agendamento():
    if not session.get('usuario_email'):
        flash("Faça login para acessar esta página.", "error")
        return redirect(url_for('login.login'))
    
    link_agenda = "barbearia-overclock-aihkmo"
    nome_usuario = session.get("usuario_nome")
    email_usuario = session.get("usuario_email")
    
    return render_template(
        'home.html', 
        link_cal=link_agenda,
        nome=nome_usuario,
        email=email_usuario
    )