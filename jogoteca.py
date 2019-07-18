from flask import Flask, render_template, request, redirect, session, flash, url_for
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
from models import Usuario, Jogo


app = Flask(__name__)
app.secret_key = 'gustavo'

app.config['MYSQL'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "************"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

#usuario1 = Usuario('gustavo', 'Gustavo Steinmetz', '1234')
#usuario2 = Usuario('Nico', 'Nico Steppat', '7a1')
#usuario3 = Usuario('marcos', 'Marcos', 'mas')

#usuarios = {usuario1.id: usuario1,
#            usuario2.id: usuario2,
#            usuario3.id: usuario3}

#jogo1 = Jogo("Counter Strike", "FPS", "PC")
#jogo2 = Jogo("World of Warcraft", "MMORPG", "PC")
#jogo3 = Jogo("Empire Earth", "Estratégia", "PC")
#lista = [jogo1, jogo2, jogo3]

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado']= usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha Inválida, tente novamente!')
            proxima_pagina = request.form['proxima']
            return redirect(url_for('login', proxima=proxima_pagina))
    else:
        flash('Não logado, tente novamente!')
        proxima_pagina = request.form['proxima']
        return redirect(url_for('login', proxima=proxima_pagina))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


app.run(debug=True)