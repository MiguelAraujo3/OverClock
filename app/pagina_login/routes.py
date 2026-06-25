from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import User
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user, UserMixin
import random

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


# fluxo de recuperação de senha

@login_route.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email_digitado = request.form.get('email')
        usuario_existe = False

        # Verifica se o e-mail existe na coluna 1 (email)
        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas[1:]: # Pula o cabeçalho
                partes = linha.strip().split(',')
                
                # 2. Mudamos para >= 4 (por segurança) e também limpamos o e-mail do CSV antes de comparar
                if len(partes) >= 4:
                    email_csv = partes[1].strip().lower()
                    
                    if email_csv == email_digitado:
                        usuario_existe = True
                        break

        if not usuario_existe:
            flash("Este e-mail não está cadastrado no sistema.")
            return redirect(url_for('login.recuperar_senha'))

        # Gera o código de 6 dígitos e salva na sessão
        codigo_verificacao = str(random.randint(100000, 999999))
        session['reset_email'] = email_digitado
        session['reset_codigo'] = codigo_verificacao

        # Importa o mail do app.py e envia o e-mail
        from main import mail 
        from flask_mail import Message
        try:
            msg = Message("Código de Recuperação - OverClock", recipients=[email_digitado])
            msg.body = f"Olá!\n\nSeu código para redefinir sua senha na OverClock é: {codigo_verificacao}\n\nSe você não solicitou essa redefinição, ignore este e-mail."
            mail.send(msg)
            flash("Um código foi enviado para o seu e-mail com sucesso! Verifique a caixa de spam.")
            return redirect(url_for('login.validar_codigo'))
        except Exception as e:
            print(e)
            flash("Erro ao enviar o e-mail. Verifique a configuração e tente novamente.")
            return redirect(url_for('login.recuperar_senha'))
    return render_template('esqueceu_senha.html')


@login_route.route('/validar-codigo', methods=['GET', 'POST'])
def validar_codigo():
    if 'reset_email' not in session or 'reset_codigo' not in session:
        flash("Sua sessão expirou. Solicite um novo código.")
        return redirect(url_for('login.recuperar_senha'))

    if request.method == 'POST':
        codigo_digitado = request.form.get('codigo')

        if codigo_digitado == session.get('reset_codigo'):
            return redirect(url_for('login.nova_senha'))
        else:
            flash("Código de verificação incorreto. Tente novamente.")
            return redirect(url_for('login.validar_codigo'))
    return render_template('validar_codigo.html')


@login_route.route('/nova-senha', methods=['GET', 'POST'])
def nova_senha():
    email_reset = session.get('reset_email')
    if not email_reset:
        flash("Sessão inválida. Inicie o processo novamente.")
        return redirect(url_for('login.recuperar_senha'))

    if request.method == 'POST':
        nova_senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar-senha')

        if nova_senha != confirmar_senha:
            flash("As senhas não coincidem. Digite novamente.")
            return redirect(url_for('login.nova_senha'))

        nova_senha_hash = generate_password_hash(nova_senha)

        # Lê todo o CSV
        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        # Sobrescreve o CSV injetando a nova senha na linha correspondente
        with open(CAMINHO_CSV, mode='w', encoding='utf-8') as arquivo:
            for linha in linhas:
                partes = linha.strip().split(',')
                # Confirma se é a linha do usuário pelo email (partes[1])
                if len(partes) >= 4 and partes[1].strip().lower() == email_reset.strip().lower():
                    # Reconstrói a linha mantendo nome, email, telefone e mudando só a senha
                    linha_atualizada = f"{partes[0]},{partes[1]},{partes[2]},{nova_senha_hash}\n"
                    arquivo.write(linha_atualizada)
                else:
                    # Se não for o usuário, apenas reescreve a linha original
                    arquivo.write(linha)

        # Limpa os dados da sessão
        session.pop('reset_email', None)
        session.pop('reset_codigo', None)

        flash("Sua nova senha foi salva! Faça o login.")
        return redirect(url_for('login.login'))    
    return render_template('nova_senha_recuperar.html')