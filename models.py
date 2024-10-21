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
    
    @classmethod
    def add (cls, nome, email, senha):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tb_usuarios (usr_nome, usr_email, usr_senha) VALUES (%s,%s,%s)', (nome,email,senha))

        conn.commit()
        conn.close()

class Tarefa:
    
    def __init__(self, nome, categoria, descricao, data, data_limite, status, prioridade, user_id):
       self.nome = nome
       self.categoria = categoria
       self.descricao = descricao
       self.data = data
       self.data_limite = data_limite
       self.status = status
       self.prioridade = prioridade  
       self.user_id = user_id


    @classmethod
    def get(cls, id):
           conn = obter_conexao()
           cursor = conn.cursor()
           cursor.execute('SELECT * FROM tb_tarefas WHERE tar_usr_id=%s',(id,))
           tarefas = cursor.fetchall()

           conn.close()

           return tarefas

    @classmethod
    def add_tarefa(cls, nome, categoria, descricao, data, data_limite, status, prioridade, user_id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tb_tarefas (tar_nome, tar_categoria, tar_descricao, tar_data, tar_data_limite, tar_status, tar_prioridade, tar_usr_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(nome, categoria, descricao, data, data_limite, status, prioridade, user_id) )

        conn.commit()
        conn.close()
    
    @classmethod
    def update_tarefa(cls, nome, categoria, descricao, data_limite, status, prioridade, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute('UPDATE tb_tarefas SET tar_nome=%s, tar_categoria=%s, tar_descricao=%s, tar_data_limite=%s, tar_status=%s, tar_prioridade=%s WHERE tar_id=%s',(nome, categoria, descricao, data_limite, status, prioridade, id) )

        conn.commit()
        conn.close()
    
    @classmethod #Opção 1
    def get_tarefa_by_nome(cls, nome, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        query = 'SELECT * FROM tb_tarefas WHERE tar_nome LIKE %s and tar_usr_id=%s'
        cursor.execute(query, (f"%{nome}%", id,))
        tarefas = cursor.fetchall()

        cursor.close()
        conn.close()

        return tarefas
    
    @classmethod #Opção 2
    def get_tarefa_by_categoria(cls, categoria, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        query = 'SELECT * FROM tb_tarefas WHERE tar_categoria=%s and tar_usr_id=%s'
        cursor.execute(query, (categoria, id,))
        tarefas = cursor.fetchall()

        cursor.close()
        conn.close()

        return tarefas
    
    @classmethod #Opção 3
    def get_tarefa_by_descricao(cls, descricao, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        query = 'SELECT * FROM tb_tarefas WHERE tar_descricao LIKE %s and tar_usr_id=%s'
        cursor.execute(query, (f"%{descricao}%", id, ))
        tarefas = cursor.fetchall()

        cursor.close()
        conn.close()

        return tarefas
    
    @classmethod #Opção 4
    def get_tarefa_by_data_limite(cls, data_limite, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        query = 'SELECT * FROM tb_tarefas WHERE tar_data_limite=%s and tar_usr_id=%s'
        cursor.execute(query, (data_limite, id,))
        tarefas = cursor.fetchall()

        cursor.close()
        conn.close()

        return tarefas
    
    @classmethod #Opção 5
    def get_tarefa_by_status(cls, status, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        query = 'SELECT * FROM tb_tarefas WHERE tar_status=%s and tar_usr_id=%s'
        cursor.execute(query, (status, id,))
        tarefas = cursor.fetchall()

        cursor.close()
        conn.close()

        return tarefas
    
    @classmethod #Opção 6
    def get_tarefa_by_prioridade(cls, prioridade, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        query = 'SELECT * FROM tb_tarefas WHERE tar_prioridade=%s and tar_usr_id=%s'
        cursor.execute(query, (prioridade, id,))
        tarefas = cursor.fetchall()

        cursor.close()
        conn.close()

        return tarefas
    
    @classmethod
    def delete_tarefa(cls, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_tarefas WHERE tar_id=%s',(id,) )

        conn.commit()
        conn.close()