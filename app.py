from flask import Flask
from app.pagina_inicial.routes import base_route
from app.pagina_agendamento.routes import agendamento_route

#Criando aplicação Flask e registrando rotas do modulo
app = Flask(__name__)

app.register_blueprint(base_route)

app.register_blueprint(agendamento_route)

if __name__ == "__main__":
    app.run(debug=True)