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
    if request.method=='POST':
        

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        User.add(nome,email,senha)

        user = User.select_get_by_email(email)
        login_user(user)

        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    texto = ''
    if request.method=='POST':

        #nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user = User.select_get_by_email(email)
        if user:
            if senha==user.senha:
                login_user(user)
                data = date.today()
                return redirect(url_for('dash', data=data))
            else:
                texto = 'Senha incorreta'
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


@app.route('/filter', methods=['GET', 'POST'])
@login_required
def filter():
    tarefas = []
    if request.method == 'POST':
        filtro = request.form['filtros']
        valor = request.form['Valor']
        if filtro == 'Nome':
            tarefas = Tarefa.get_tarefa_by_nome(valor)
        elif filtro == 'Categoria':
            tarefas = Tarefa.get_tarefa_by_categoria(valor)
        elif filtro == 'Descrição':
            tarefas = Tarefa.get_tarefa_by_descricao(valor)
        elif filtro == 'Prazo':
            tarefas = Tarefa.get_tarefa_by_data_limite(valor)
        elif filtro == 'Status':
            tarefas = Tarefa.get_tarefa_by_status(valor)
        elif filtro == 'Prioridade':
            tarefas = Tarefa.get_tarefa_by_prioridade(valor)

        return render_template('filter.html', tarefas=tarefas)
    
    return render_template('filter.html', tarefas=tarefas)
        

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