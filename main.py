from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user # "LoginManager" necessário para o gerenciamento do sistema de logins; "login_user" responsável por logar o usuario, sua instancia está localizada na rota "registrar"; "login_required" serve para tornar as rotas acessíveis apenas se o usuário estiver logado; "logout_user" serve para adicionar a função de logout; "current_user" serve para manter o mesmo usuário logado mesmo que a página seja recarregada, também é possível printar senha e login com essa classe podendo deixa-la nos arquivos html como no exemplo feito no arquivo home.html
from models import usuario
from db import db
import hashlib # serve para criptografar os dados da tabela do banco de dados, é possível fazer a mesma coisa importando um modo proprio do flask

app = Flask(__name__)
app.secret_key = 'lancode' # necessário para que o login funcione, para segurança do projeto é necessário que o valor seja declarado dentro de um arquivo dotenv
lm = LoginManager(app)
lm.login_view = 'login'# redireciona para página de login quando a senha e login estão errados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app) 

# CRIPTOGRAFIA
def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8')) # essa linha de codigo cria uma instância para a biblioteca da "hashlib" e ao escolher o formato de encriptação "sha256" você encripta os dados, "txt.encode()" transforma a string em formato de bits. "'utf-8'" é um formato que faz a criptografia aceitar acentos na criptografias
    return hash_obj.hexdigest() # retorna o hash_obj transformando-o em uma string
print('esse é o hash' + hash('oi')) # print de exemplo do resultado da função hash

@lm.user_loader
def user_loader(id): # essas duas linhas irão definir como o sistema irá resgatar suas informações usando o id como parametro
    Usuario = db.session.query(usuario).filter_by(id=id).first() # única utilidade dessa linha é pegar os dados referentes ao id do usuário
    return Usuario


@app.route('/')
@login_required # a rota onde esse decorator se localiza só pode ser acessada se o usuário estiver logado
def home():
    return render_template('home.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        user = db.session.query(usuario).filter_by(nome=nome, senha=hash(senha)).first() # o filtro impõe a condição de que para acessar os dados da tabela será necessário que a senha e o nome estejam corretos; "senha=hash(senha)" o valor que foi encriptado na rota registrar será o mesmo valor digitado aqui caso a senha digitada seja a mesma
        if not user: # se os dados do POST não baterem com o que está no banco de dados então o retorno será 'Nome ou senha incorretos'
            return 'Nome ou senha incorretos'
        
        login_user(user) # caso os dados do POST sejam os mesmos dos dados da tabela a variável usuário servirá como argumento para a instância de "login_user()" para que dessa forma você seja logado
        return redirect(url_for('home')) # aqui você será redirecionado para página home

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user() # instância da classe logout importada de flask login
    return redirect(url_for('home'))

# REGISTRAR
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        novo_usuario = usuario(nome=nome, senha=hash(senha)) # 'senha=hash(senha)' está jogando o valor digitado no registro para a função hash que encripta o valor 
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario) # instancia importada de "flask_login" com a funcionalidade de logar o usuario, para que isso funcione é necessário importar o "UserMixin" no arquivo que guarda a classe, neste caso o arquivo é "models.py" e também é necessário criar uma "secret key" essa por sua vez está localizada abaixo da linha "app = Flask(__name__)" 

        # IMPORTANTE:
        # é obrigatório em todas as rotas inserir um retorno para que a aplicação funcione
        return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 