from flask import Blueprint, render_template

#Estrutura da rota da página inicial
login_route = Blueprint('login', __name__)

@login_route.route('/login', methods=["POST","GET"])
def login():
    return render_template('login.html')