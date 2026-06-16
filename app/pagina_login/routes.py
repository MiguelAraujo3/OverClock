from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import User
import os
from werkzeug.security import check_password_hash
from flask_login import login_user, UserMixin

login_route = Blueprint('login_route', __name__)

CAMINHO_CSV = os.path.join('data', 'dados.csv')

class UsuarioLogado(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id 
        self.nome = nome
        self.email = email

@login_route.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        arquivo_existe = os.path.isfile(CAMINHO_CSV)

        if not arquivo_existe:
            flash("Nenhuma conta encontrada com este e-mail. Crie uma conta primeiro!")
            return redirect(url_for('cadastro.cadastro'))

        usuario = None

        # Lendo o arquivo csv
        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo_leitura:
            linhas = arquivo_leitura.readlines()
            
            for linha in linhas[1:]: # Pula o cabeçalho
                partes = linha.strip().split(',')
                
                if len(partes) >= 4:
                    if partes[1] == email: # Índice 1 é o e-mail
                        usuario = {
                            'nome': partes[0],
                            'email': partes[1],
                            'telefone': partes[2],
                            'senha': partes[3] # Índice 3 é o hash da senha
                        }
                        break

        if usuario is None:
            flash("Este e-mail não está cadastrado no sistema.")
            return redirect(url_for('login_route.login'))

        senha_hash_salva = usuario.get('senha')
        
        if not check_password_hash(senha_hash_salva, senha):
            flash("Senha incorreta. Tente novamente.")
            return redirect(url_for('login_route.login'))

        usuario_obj = UsuarioLogado(
            id=usuario.get('email'), 
            nome=usuario.get('nome'),
            email=usuario.get('email')
        )
        
        login_user(usuario_obj)
        
        session["usuario_nome"] = usuario.get("nome")
        session["usuario_email"] = usuario.get("email")

        proxima_pagina = request.args.get('next')
        if proxima_pagina:
            return redirect(proxima_pagina)
            
        return redirect(url_for('agendamento.agendamento'))
    
    return render_template('login.html')