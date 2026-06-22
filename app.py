from flask import Flask
from flask_login import LoginManager

#Criando aplicação Flask e registrando rotas do modulo
app = Flask(__name__)

#Secret key
app.secret_key = 'OVERCLOCKZANDO'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'
login_manager.login_message = 'Faça login para acessar esta página.'
from app.pagina_login import buscar_usuario_no_csv
login_manager.user_loader(buscar_usuario_no_csv)

from app.pagina_inicial.routes import base_route
from app.pagina_agendamento.routes import agendamento_route
from app.pagina_login.routes import login_route
from app.pagina_cadastro.routes import cadastro_route

app.register_blueprint(base_route)
app.register_blueprint(agendamento_route)
app.register_blueprint(login_route)
app.register_blueprint(cadastro_route)



if __name__ == "__main__":
    app.run(debug=True)