from flask import Flask, render_template, request, redirect, url_for
import pymysql
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User, obter_conexao, Tarefa
from datetime import date

login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MUITODIFICIL'


login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET','POST'])
def register():
    registro =''
    if request.method=='POST':
        

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        

        
        user = User.select_get_by_email(email)  
        if user:
            
            registro = 'Email já cadastrado no sistema'
            return render_template('register.html', registro=registro)

        else:
            User.add(nome,email,senha)
            registro = 'Registrado com sucesso'
            user = User.select_get_by_email(email)
            login_user(user)

            return render_template('login.html', registro=registro)
        
        
        
    return render_template('register.html',registro=registro)


@app.route('/login',methods=['GET','POST'])
def login():
    texto = ''
    if request.method=='POST':

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user = User.select_get_by_email(email)
        if user:
            if senha==user.senha and user.nome==nome:
                login_user(user)
                data = date.today()
                return redirect(url_for('dash', data=data))
            else:
                texto = 'Senha ou usuário incorretos'
                return render_template('login.html',texto=texto)
                
        else:
            texto = 'Usuário ou email inválidos'
    return render_template('login.html',texto=texto)


@app.route('/dash')
@login_required
def dash():
    user_id = current_user.id
    
    tarefas = Tarefa.get(user_id)
    return render_template('dash.html', tarefas=tarefas)


@app.route('/select', methods=['GET', 'POST'])
@login_required
def select():
    user_id = current_user.id
    if request.method=='POST':
        status = request.form['status']
        data = request.form['data']
        prioridade = request.form['prioridade']
        palavras = request.form['palavras']
        categoria = request.form['categoria']
        
        conn = obter_conexao()
        cursor = conn.cursor()
        query = ('SELECT * FROM tb_tarefas WHERE tar_usr_id=%s')
        params = [user_id]
        
        if status and status !='Todos':
            query += ' AND tar_status=%s'
            params.append(status)
        if data:
            query += ' AND tar_data_limite=%s'
            params.append(data)
        if prioridade and prioridade !='Todos':
            query += ' AND tar_prioridade=%s'
            params.append(prioridade)
        if palavras :
            query += ' AND tar_descricao LIKE %s'
            params.append(f'%{palavras}%')
        if categoria and categoria != 'Todas':
            query += ' AND tar_categoria=%s'
            params.append(categoria)
        
        cursor.execute(query,params)
        tarefas = cursor.fetchall()
        conn.close()
        
        return render_template('dash.html', tarefas=tarefas)
    return render_template('dash.html')
        

@app.route('/add',methods=['GET','POST'])
@login_required
def add():
    if request.method=='POST':
        id = current_user.id
        data = date.today()
        
        nome = request.form['nome']
        categoria = request.form['categoria']
        desc = request.form['desc']
        data_limite = request.form['data_limite']
        status = request.form['status']
        prioridade = request.form['prioridade']

        try:
            Tarefa.add_tarefa(nome, categoria, desc, data, data_limite, status, prioridade, id)
            return redirect(url_for('dash'))
        except:
            return f'Não foi possível adicionar sua tarefa, {id}'
        
    return render_template('add.html')


@app.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        desc = request.form['desc']
        data_limite = request.form['data_limite']
        status = request.form['status']
        prioridade = request.form['prioridade']

        Tarefa.update_tarefa(nome, categoria, desc, data_limite, status, prioridade, id)
        return redirect(url_for('dash'))
    return render_template('update.html')


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    Tarefa.delete_tarefa(id)
    return redirect(url_for('dash'))
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))