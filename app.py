from flask import Flask
from app.pagina_inicial.routes import base_route

#Criando aplicação Flask e registrando rotas do modulo
app = Flask(__name__)

app.register_blueprint(base_route)

if __name__ == "__main__":
    app.run(debug=True)