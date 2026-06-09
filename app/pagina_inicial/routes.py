from flask import Blueprint, render_template

#Estrutura da rota da página inicial
base_route = Blueprint('home', __name__)

@base_route.route('/')
def home():
    return render_template('base.html')