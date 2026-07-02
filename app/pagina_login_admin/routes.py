from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import User
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user, UserMixin, logout_user
import random

login_route_admin = Blueprint('login_admin', __name__)

CAMINHO_CSV = 'data/dados.csv'

class UsuarioLogado(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id 
        self.nome = nome
        self.email = email

@login_route_admin.route('/admin', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = None

        # Lendo o arquivo csv
        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo_leitura:
            linhas = arquivo_leitura.readlines()
            
            if len(linhas) > 1:
                partes = linhas[1].strip().split(',')
                
                if partes[1] == email: # Índice 1 é o e-mail
                    usuario = {
                        'nome': partes[0],
                        'email': partes[1],
                        'telefone': partes[2],
                        'senha': partes[3] # Índice 3 é o hash da senha
                    }

        if usuario is None:
            flash("Este e-mail não é de um administrador.", "error")
            return redirect(url_for('login_admin.login'))

        senha_hash_salva = usuario.get('senha')
        
        if not check_password_hash(senha_hash_salva, senha):
            flash("Senha incorreta. Tente novamente.", "error")
            return redirect(url_for('login_admin.login'))

        usuario_obj = UsuarioLogado(
            id=usuario.get('email'), 
            nome=usuario.get('nome'),
            email=usuario.get('email')
        )
        
        login_user(usuario_obj)
        
        session["usuario_nome"] = usuario.get("nome")
        session["usuario_email"] = usuario.get("email")
            
        return redirect(url_for('dashboard.dashboard')) 
    
    return render_template('login_admin.html')

#SAIR DA CONTA
@login_route_admin.route('/logout_admin')
def logout():
    session.clear()
    session.pop('usuario_nome', None)
    session.pop('usuario_email', None)
    
    flash("Você saiu da sua conta com sucesso.", "success")
    return redirect(url_for('login_admin.login'))
