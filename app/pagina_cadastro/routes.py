from flask import Blueprint, render_template

#Estrutura da rota da página inicial
cadastro_route = Blueprint('cadastro', __name__)

@cadastro_route.route('/cadastro', methods=["POST","GET"])
def cadastro():
    return render_template('cadastro.html')