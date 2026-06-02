#Modulo usado para rodar a aplicação em produção
import runpy

# Força o Python a ler o arquivo físico app.py, ignorando a pasta de mesmo nome
contexto = runpy.run_path("app.py")
app = contexto["app"]