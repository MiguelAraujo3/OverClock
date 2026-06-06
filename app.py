from flask import Flask
from app.pagina_inicial.routes import base_route
from app.pagina_agendamento.routes import agendamento_route
from app.pagina_login.routes import login_route
from app.pagina_cadastro.routes import cadastro_route

#Criando aplicação Flask e registrando rotas do modulo
app = Flask(__name__)

app.register_blueprint(base_route)

app.register_blueprint(agendamento_route)

app.register_blueprint(login_route)

app.register_blueprint(cadastro_route)

#Secret key
app.secret_key = 'OVERCLOCKZANDO'

if __name__ == "__main__":
    app.run(debug=True)