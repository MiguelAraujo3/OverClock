import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Criando aplicação Flask e registrando rotas do modulo
app = Flask(__name__)

# Pegando a Secret key do .env
app.secret_key = os.getenv('SECRET_KEY')
# CONFIGURAÇÕES DO FLASK-MAIL

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Pegando os dados de e-mail do .env
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')


# Inicializa o Mail na aplicação
mail = Mail(app)

# CONFIGURAÇÕES DO FLASK-LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'
login_manager.login_message = 'Faça login para acessar esta página.'

from app.pagina_login import buscar_usuario_no_csv
login_manager.user_loader(buscar_usuario_no_csv)


# REGISTRO DE BLUEPRINTS (ROTAS)
from app.pagina_inicial.routes import base_route
from app.pagina_agendamento.routes import agendamento_route
from app.pagina_login.routes import login_route
from app.pagina_cadastro.routes import cadastro_route
from app.pagina_trocar_senha.routes import alterar_senha_route
from app.pagina_login_admin.routes import login_route_admin

app.register_blueprint(base_route)
app.register_blueprint(agendamento_route)
app.register_blueprint(login_route)
app.register_blueprint(cadastro_route)
app.register_blueprint(alterar_senha_route)
app.register_blueprint(login_route_admin)

if __name__ == "__main__":
    app.run(debug=True)