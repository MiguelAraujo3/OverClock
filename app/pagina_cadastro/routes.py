from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
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
        
        # Validando campos nulos por segurança
        if not nome or not email or not telefone or not senha or not confirmar_senha:
            flash("Por favor, preencha todos os campos do formulário.", "error")
            return redirect(url_for('cadastro.cadastro'))
        
        # Verificando se tem número no nome.
        for caractere in nome:
            if caractere.isdigit():
                flash("O nome não pode conter números. Por favor, digite um nome válido.", "error")
                return redirect(url_for('cadastro.cadastro'))

        for caractere in telefone:
            if caractere.isalpha():
                flash("O número não pode conter letras. Por favor digite um número válido", "error")
                return redirect(url_for('cadastro.cadastro'))

        # Padronizar telefone para ter exatamente 11 números
        # Isso remove parênteses, espaços e traços, deixando apenas os números (ex: 83988887777)
        telefone_limpo = ''.join(filter(str.isdigit, telefone))

        if len(telefone_limpo) != 11:
            flash("O telefone deve conter exatamente 11 números, incluindo o DDD.", "error")
            return redirect(url_for('cadastro.cadastro'))
        
        # Devolve a variavel telefone agora padronizado
        telefone = f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
               
        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres. Tente novamente.", "error")
            return redirect(url_for('cadastro.cadastro'))

        if senha != confirmar_senha:
            flash("As senhas não coincidem. Tente novamente.", "error")
            return redirect(url_for('cadastro.cadastro'))

        senha_criptografada = generate_password_hash(senha)
        
        os.makedirs('data', exist_ok=True)
        arquivo_existe = os.path.isfile(CAMINHO_CSV)

        # Verificando se tem email no banco de dados (leitura manual)
        if arquivo_existe and os.path.getsize(CAMINHO_CSV) > 0:
            with open(CAMINHO_CSV, mode='r', encoding='utf-8') as arquivo_leitura:
                linhas = arquivo_leitura.readlines()
                for linha in linhas[1:]: # Pula cabeçalho
                    partes = linha.strip().split(',')
                    if len(partes) >= 4 and partes[1] == email:
                        flash("Este e-mail já está cadastrado. Tente fazer login ou use outro e-mail.", "error")
                        return redirect(url_for('cadastro.cadastro'))

        # Escrevendo no arquivo texto manualmente (Modo Append)
        with open(CAMINHO_CSV, mode='a', encoding='utf-8') as arquivo:
            # Se não existe ou está vazio, escreve o cabeçalho primeiro
            if not arquivo_existe or os.path.getsize(CAMINHO_CSV) == 0:
                arquivo.write("nome,email,telefone,senha\n")

            # Escreve a nova linha montando a string separada por vírgulas
            nova_linha = f"{nome},{email},{telefone},{senha_criptografada}\n"
            arquivo.write(nova_linha)

        flash("Cadastro realizado com sucesso! Faça seu login.", "success")
        return redirect(url_for('login.login')) 

    return render_template('cadastro.html')