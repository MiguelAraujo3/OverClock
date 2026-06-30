import os
from flask import abort, render_template, url_for, redirect, flash
from flask_login import current_user
from . import dashboard_route

@dashboard_route.route('/dashboard')
def dashboard():

    if not current_user.is_authenticated:
        flash("Faça login como administrador para acessar essa página.", "error")
        return redirect(url_for('login_admin.login'))
    
    email_admin = os.getenv('MAIL_USERNAME')
    
    if current_user.email != email_admin: # Verifica se o usuário logado é o administrador
        flash("Faça login para acessar essa página.", "error")
        return redirect(url_for('login_admin.login'))  # Redireciona para a página de login do administrador

    caminho_csv = os.path.join('data', 'dados.csv')
    clientes_lista = []
    
    if os.path.exists(caminho_csv):
        with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            
            if len(linhas) > 1:
                for linha in linhas[2:]:
                    partes = linha.strip().split(',')
                    if len(partes) >= 4:
                        clientes_lista.append({
                            'nome': partes[0].strip(),
                            'email': partes[1].strip(),
                            'numero': partes[2].strip()
                        })
                        
    return render_template('dashboard.html', clientes=clientes_lista)