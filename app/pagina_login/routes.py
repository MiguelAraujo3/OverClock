from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import User
import os
import csv
from werkzeug.security import check_password_hash
from flask_login import login_user, UserMixin

login_route = Blueprint('login_route', __name__)

CAMINHO_CSV = os.path.join('data', 'dados.csv')
class UsuarioLogado(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id # O Flask-Login precisa de um ID único (vamos usar o email)
        self.nome = nome
        self.email = email


@login_route.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        arquivo_existe = os.path.isfile(CAMINHO_CSV)

        # 1. Se o arquivo CSV sequer existe, significa que ninguém nunca se cadastrou
        if not arquivo_existe:
            flash("Nenhuma conta encontrada com este e-mail. Crie uma conta primeiro!")
            return redirect(url_for('cadastro.cadastro'))

        # 2. Vamos ler o CSV para procurar o usuário
        usuario = None

        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo_leitura:
            leitor = csv.DictReader(arquivo_leitura)
            for linha in leitor:
                if linha.get('email') == email:
                    usuario = linha
                    break

        # 3. VALIDAÇÃO: Se o e-mail não foi encontrado no loop anterior
        if usuario is None:
            flash("Este e-mail não está cadastrado no sistema.")
            return redirect(url_for('login_route.login'))

        # 4. VALIDAÇÃO DA SENHA: Usando a função correta para comparar hashes
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
        #Salvando informações na session
        session["usuario_nome"] = usuario.get("nome")
        session["usuario_email"] = usuario.get("email")

        flash(f"Bem-vindo de volta, {usuario.get('nome')}!")
        proxima_pagina = request.args.get('next')
        if proxima_pagina:
            return redirect(proxima_pagina)
        return redirect(url_for('agendamento.agendamento'))
    
    return render_template('login.html')