from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os 

alterar_senha_route = Blueprint('alterar_senha', __name__)
CAMINHO_CSV = os.path.join('data', 'dados.csv')

@alterar_senha_route.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():

    if request.method == 'POST':

        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        # Verifica se todos os campos foram preenchidos
        if not senha_atual or not nova_senha or not confirmar_senha:
            flash("Preencha todos os campos.", "error")
            return redirect(url_for('alterar_senha.alterar_senha'))

        # Verifica se a nova senha e a confirmação são iguais
        if nova_senha != confirmar_senha:
            flash("As novas senhas não coincidem.", "error")
            return redirect(url_for('alterar_senha.alterar_senha'))

        # Verifica o tamanho da nova senha
        if len(nova_senha) < 8:
            flash("A nova senha deve conter pelo menos 8 caracteres.", "error")
            return redirect(url_for('alterar_senha.alterar_senha'))

        # Lê todo o CSV
        with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        # ======= VALIDAÇÕES =======

        for linha in linhas[1:]:

            partes = linha.strip().split(',')

            if partes[1].strip().lower() == current_user.email.strip().lower():

                # Verifica se a senha atual está correta
                if not check_password_hash(partes[3], senha_atual):
                    flash("Senha atual incorreta.", "error")
                    return redirect(url_for('alterar_senha.alterar_senha'))

                # Verifica se a nova senha é igual à antiga
                if check_password_hash(partes[3], nova_senha):
                    flash("A nova senha deve ser diferente da senha atual.", "error")
                    return redirect(url_for('alterar_senha.alterar_senha'))

                break

        # Gera o hash somente depois de todas as validações
        nova_senha_hash = generate_password_hash(nova_senha)

        # ======= ESCRITA =======

        with open(CAMINHO_CSV, mode='w', encoding='utf-8') as arquivo:

            arquivo.write(linhas[0])

            for linha in linhas[1:]:

                partes = linha.strip().split(',')

                if partes[1].strip().lower() == current_user.email.strip().lower():
                    linha = f"{partes[0]},{partes[1]},{partes[2]},{nova_senha_hash}\n"

                arquivo.write(linha)

        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for('alterar_senha.alterar_senha'))  

    return render_template('alterar_senha.html')
