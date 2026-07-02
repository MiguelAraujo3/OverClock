from flask import Blueprint, render_template, redirect, session, url_for
from flask_login import current_user  # Importa o gerenciador do usuário atual

# Estrutura da rota da página inicial
base_route = Blueprint('home', __name__)

@base_route.route('/')
def home():
        
    return render_template('home.html')
