from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import csv
import os

cadastro_route = Blueprint('cadastro', __name__)

CAMINHO_CSV = os.path.join('data', 'dados.csv')

@cadastro_route.route('/cadastro', methods=["POST", "GET"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar-senha')
               
        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres. Tente novamente.")
            return redirect(url_for('cadastro.cadastro'))

        #Criptografando senha.
        if senha != confirmar_senha:
            flash("As senhas não coincidem. Tente novamente.")
            return redirect(url_for('cadastro.cadastro'))

        senha_criptografada = generate_password_hash(senha)
        #Verificar se o arquivo data existe.
        os.makedirs('data', exist_ok=True)

        arquivo_existe = os.path.isfile(CAMINHO_CSV)
        #Verificando se tem email no banco de dados.
        if arquivo_existe:
            with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo_leitura:
                leitor = csv.DictReader(arquivo_leitura)
                for linha in leitor:
                    if linha.get('email') == email:
                        flash("Este e-mail já está cadastrado. Tente fazer login ou use outro e-mail.")
                        return redirect(url_for('cadastro.cadastro'))

        #Atualizando arquivo CSV com o modo "a" e enconding "utf-8" para caracteres
        with open(CAMINHO_CSV, mode='a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            
            if not arquivo_existe:
                writer.writerow(['nome', 'email', 'telefone', 'senha'])

            writer.writerow([nome, email, telefone, senha_criptografada])
        flash("Cadastro realizado com sucesso! Faça seu login.")
        return redirect(url_for('login_route.login')) 

    return render_template('cadastro.html')