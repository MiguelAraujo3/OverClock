from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import User
from werkzeug.security import check_password_hash
from flask_login import login_user, UserMixin

login_route = Blueprint('login', __name__)

CAMINHO_CSV = 'data/dados.csv'

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

        usuario = None

        # Lendo o arquivo csv
        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo_leitura:
            linhas = arquivo_leitura.readlines()
            
            for linha in linhas[1:]: # Pula o cabeçalho
                partes = linha.strip().split(',')
                
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
            return redirect(url_for('login.login'))

        senha_hash_salva = usuario.get('senha')
        
        if not check_password_hash(senha_hash_salva, senha):
            flash("Senha incorreta. Tente novamente.")
            return redirect(url_for('login.login'))

        usuario_obj = UsuarioLogado(
            id=usuario.get('email'), 
            nome=usuario.get('nome'),
            email=usuario.get('email')
        )
        
        login_user(usuario_obj)
        
        session["usuario_nome"] = usuario.get("nome")
        session["usuario_email"] = usuario.get("email")
            
        return redirect(url_for('agendamento.agendamento'))
    
    return render_template('login.html')

#SAIR DA CONTA
@login_route.route('/logout')
def logout():

    session.pop('usuario_nome', None)
    session.pop('usuario_email', None)
    
    flash("Você saiu da sua conta com sucesso.")
    return redirect(url_for('login.login'))

#EXCLUSÃO DE CONTA
@login_route.route('/excluir_conta', methods=['POST'])
def excluir_conta():
    email_para_excluir = session.get('usuario_email')
    
    # Segurança: se a sessão estiver vazia, bloqueia a ação
    if not email_para_excluir:
        flash("Você precisa estar logado para excluir uma conta.")
        return redirect(url_for('login_route.login'))

    # Lê o CSV atual direto
    with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
        
    # Abre novamente para sobrescrever
    with open(CAMINHO_CSV, mode='w', encoding='utf-8') as arquivo:
        for linha in linhas:
            partes = linha.strip().split(',')

            if partes[1] != email_para_excluir:
                arquivo.write(linha)

    # Destrói a sessão por completo, finalizando a exclusão e o acesso
    session.pop('usuario_nome', None)
    session.pop('usuario_email', None)
    
    flash("Sua conta foi excluída definitivamente.")
    return redirect(url_for('home.home'))