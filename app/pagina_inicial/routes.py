from flask import Blueprint, render_template, redirect, session, url_for
from flask_login import current_user  # Importa o gerenciador do usuário atual

# Estrutura da rota da página inicial
base_route = Blueprint('home', __name__)

@base_route.route('/')
def home():
    if session.get('usuario_email'):
        # Se tem e-mail, o usuário está logado! Manda pro agendamento.
        return redirect(url_for('agendamento.agendamento'))
    # Se não estiver logado, renderiza a página inicial/base normalmente
    return render_template('base.html')