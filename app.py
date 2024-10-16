from flask import Flask, render_template, request, redirect, url_for
import pymysql
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User

login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MUITODIFICIL'

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'database' : 'db_projeto',
}

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method=='POST':
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        cursor.execute('INSERT INTO tb_usuarios (usr_nome,usr_email,usr_senha) VALUES (%s,%s,%s)', (nome,email,senha))
        conn.commit()
        conn.close()

        user = User.select_get_by_email(email)
        login_user(user)

        return redirect(url_for('index'))
    return render_template('registro.html')

@app.route('/login',methods=['GET','POST'])
def login():
    texto = ''
    if request.method=='POST':

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user = User.select_get_by_email(email)
        if user:
            if senha==user.senha:
                login_user(user)
                return redirect(url_for('dash'))
            else:
                texto = 'Senha incorreta'
                return render_template('login.html',texto=texto)
                
        else:
            texto = 'Usuário ou email inválidos'
    return render_template('login.html',texto=texto)
    
        
        
 
    
@app.route('/dash',methods=['GET','POST'])
@login_required
def dash():
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT tar_nome,tar_descricao,tar_status, tar_data, tar_data_limite FROM tb_tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    return render_template('dash.html',tarefas=tarefas)


