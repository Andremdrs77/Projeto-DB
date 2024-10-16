import pymysql
from flask_login import UserMixin

def obter_conexao():
    db_config = {
        'user' :   'root',
        'password' : '',
        'host' : 'localhost',
        'database' : 'db_projeto'
    }
    return pymysql.connect(**db_config)

class User(UserMixin):
    id : str

    def __init__(self, nome, email, senha):
       self.nome = nome
       self.email = email
       self.senha = senha
    
    @classmethod
    def get(cls,id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM tb_usuarios WHERE usr_id=%s',(id,))
        dados = cursor.fetchone()
        cursor.close()
        conexao.close()

        if dados:
            user = User(dados[1],dados[2],dados[3])
            user.id = dados[0]
        else:
            dados = None
        return user

    @classmethod
    def select_get_by_email(cls,email):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM tb_usuarios WHERE usr_email=%s', (email,))
        dados = cursor.fetchone()
        cursor.close()
        conexao.close()

        if dados:
            user = User(dados[1],dados[2],dados[3])
            user.id = dados[0]
        else:
            user=None
            dados = None
        return user
        