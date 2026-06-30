from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, UserMixin, logout_user
import random

login_route = Blueprint('login', __name__)

CAMINHO_CSV = 'data/dados.csv'

class UsuarioLogado(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id 
        self.nome = nome
        self.email = email

@login_route.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha')

        usuario = None

        # Lendo o arquivo csv com tratamento de erro
        try:
            with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo_leitura:
                linhas = arquivo_leitura.readlines()
                
                # CORREÇÃO: linhas[2:] pula apenas a primeira linha (cabeçalho e conta do admin)
                for linha in linhas[2:]: 
                    partes = linha.strip().split(',')
                    
                    # CORREÇÃO: Verifica se a linha é válida antes de ler o índice
                    if len(partes) >= 4 and partes[1].strip().lower() == email:
                        usuario = {
                            'nome': partes[0],
                            'email': partes[1],
                            'telefone': partes[2],
                            'senha': partes[3]
                        }
                        break
        except FileNotFoundError:
            flash("Erro interno: Banco de dados não encontrado.", "error")
            return redirect(url_for('login.login'))

        if usuario is None:
            flash("Este e-mail não está cadastrado no sistema.", "error")
            return redirect(url_for('login.login'))

        senha_hash_salva = usuario.get('senha')
        
        if not check_password_hash(senha_hash_salva, senha):
            flash("Senha incorreta. Tente novamente.", "error")
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


@login_route.route('/logout')
def logout():
    logout_user()
    session.clear() 
    flash("Você saiu da sua conta com sucesso.", "success")
    return redirect(url_for('login.login'))


@login_route.route('/excluir_conta', methods=['POST'])
def excluir_conta():
    email_para_excluir = session.get('usuario_email')
    
    if not email_para_excluir:
        flash("Você precisa estar logado para excluir uma conta.", "error")
        return redirect(url_for('login.login'))

    try:
        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            
        with open(CAMINHO_CSV, mode='w', encoding='utf-8') as arquivo:
            for linha in linhas:
                partes = linha.strip().split(',')
                # CORREÇÃO: Proteção contra linhas vazias e mantém o cabeçalho intacto
                if len(partes) >= 2:
                    if partes[1].strip().lower() == email_para_excluir.strip().lower():
                        continue # Pula a linha do usuário (deleta)
                arquivo.write(linha)
    except Exception:
        flash("Erro ao tentar excluir a conta. Tente novamente mais tarde.", "error")
        return redirect(url_for('agendamento.agendamento'))

    logout_user()
    session.clear()
    
    flash("Sua conta foi excluída definitivamente.", "success")
    return redirect(url_for('home.home'))


# --- FLUXO DE RECUPERAÇÃO DE SENHA ---

@login_route.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    email_digitado = None

    if request.method == 'POST':
        email_digitado = request.form.get('email', '').strip().lower()
    else:
        email_url = request.args.get('email')
        if email_url:
            email_digitado = email_url.strip().lower()

    if email_digitado:
        usuario_existe = False

        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas[1:]:
                partes = linha.strip().split(',')
                if len(partes) >= 2:
                    if partes[1].strip().lower() == email_digitado:
                        usuario_existe = True
                        break

        if not usuario_existe:
            flash("Este e-mail não está cadastrado no sistema.", "error")
            return redirect(url_for('login.recuperar_senha'))

        codigo_verificacao = str(random.randint(100000, 999999))
        session['reset_email'] = email_digitado
        session['reset_codigo'] = codigo_verificacao
        session['codigo_validado'] = False # CORREÇÃO: Reseta a validação de segurança

        from main import mail 
        from flask_mail import Message
        try:
            msg = Message("Código de Recuperação - OverClock", recipients=[email_digitado])
            msg.body = f"Olá!\n\nSeu código para redefinir sua senha na OverClock é: {codigo_verificacao}\n\nSe você não solicitou essa redefinição, ignore este e-mail."
            mail.send(msg)
            
            flash("Um código foi enviado para o seu e-mail com sucesso!", "success")
            # CORREÇÃO: Redireciona em vez de renderizar direto (evita reenvio com F5)
            return redirect(url_for('login.validar_codigo'))
            
        except Exception as e:
            print(e)
            flash("Erro ao enviar o e-mail. Verifique a configuração.", "error")
            return redirect(url_for('login.recuperar_senha'))

    return render_template('esqueceu_senha.html')


@login_route.route('/validar-codigo', methods=['GET', 'POST'])
def validar_codigo():
    if 'reset_email' not in session or 'reset_codigo' not in session:
        flash("Sua sessão expirou. Solicite um novo código.", "error")
        return redirect(url_for('login.recuperar_senha'))

    if request.method == 'POST':
        codigo_digitado = request.form.get('codigo')

        if codigo_digitado == session.get('reset_codigo'):
            session['codigo_validado'] = True # CORREÇÃO: Libera o acesso à próxima rota
            return redirect(url_for('login.nova_senha'))
        else:
            flash("Código de verificação incorreto. Tente novamente.", "error")
            return redirect(url_for('login.validar_codigo'))
            
    # CORREÇÃO: Passa o e-mail para o template para a opção de "Reenviar Código" funcionar
    return render_template('validar_codigo.html', email=session.get('reset_email'))


@login_route.route('/nova-senha', methods=['GET', 'POST'])
def nova_senha():
    email_reset = session.get('reset_email')
    # CORREÇÃO: Se não validou o código, barra o acesso por segurança
    if not email_reset or not session.get('codigo_validado'):
        flash("Acesso não autorizado. Valide seu código primeiro.", "error")
        return redirect(url_for('login.recuperar_senha'))

    if request.method == 'POST':
        nova_senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar-senha')

        if nova_senha != confirmar_senha:
            flash("As senhas não coincidem. Digite novamente.", "error")
            return redirect(url_for('login.nova_senha'))

        nova_senha_hash = generate_password_hash(nova_senha)

        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        with open(CAMINHO_CSV, mode='w', encoding='utf-8') as arquivo:
            for linha in linhas:
                partes = linha.strip().split(',')
                if len(partes) >= 4 and partes[1].strip().lower() == email_reset.strip().lower():
                    linha_atualizada = f"{partes[0]},{partes[1]},{partes[2]},{nova_senha_hash}\n"
                    arquivo.write(linha_atualizada)
                else:
                    arquivo.write(linha)

        # CORREÇÃO: Limpa todas as variáveis temporárias de segurança
        session.pop('reset_email', None)
        session.pop('reset_codigo', None)
        session.pop('codigo_validado', None)

        flash("Sua nova senha foi salva! Faça o login.", "success")
        return redirect(url_for('login.login'))    
        
    return render_template('nova_senha_recuperar.html')