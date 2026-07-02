from flask_login import UserMixin
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
        linhas = arquivo.readlines()
        
        # Ignora o arquivo se só tiver o cabeçalho ou for vazio
        if len(linhas) <= 1:
            return None
            
        for linha in linhas[1:]:
            # .strip() remove espaços vazios e \n, .split(',') corta nos textos
            partes = linha.strip().split(',')
            
            # Garante que a linha tem as 4 colunas (nome, email, telefone, senha)
            if len(partes) >= 4:
                email_csv = partes[1]
                if email_csv == user_id:
                    nome_csv = partes[0]
                    return User(id=email_csv, nome=nome_csv, email=email_csv)
                    
    return None