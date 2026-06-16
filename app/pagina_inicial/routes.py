from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user  # Importa o gerenciador do usuário atual

# Estrutura da rota da página inicial
base_route = Blueprint('home', __name__)

@base_route.route('/')
def home():
    # Se o usuário já estiver autenticado (logado), manda ele direto para o agendamento
    if current_user.is_authenticated:
        return redirect(url_for('agendamento.agendamento'))
    
    # Se não estiver logado, renderiza a página inicial/base normalmente
    return render_template('base.html')