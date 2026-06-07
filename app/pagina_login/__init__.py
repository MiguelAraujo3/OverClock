from flask_login import UserMixin
import csv
import os

class User(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email


def buscar_usuario_no_csv(user_id):
    caminho_csv = os.path.join('data', 'dados.csv')
    if not os.path.exists(caminho_csv):
        return None 
    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        for linha in leitor_csv:
            if linha.get('email') == user_id:
                return User(id=linha['email'], nome=linha['nome'], email=linha['email'])
    return None