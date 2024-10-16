from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'database' : 'db_projeto',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        cursor.execute('INSERT INTO tb_usuarios (usr_nome,usr_email,usr_senha) VALUES (%s,%s,%s)', (nome,email,senha))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('register.html')


