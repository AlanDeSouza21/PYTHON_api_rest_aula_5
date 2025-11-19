from db import db
from flask_login import UserMixin

class usuario(UserMixin, db.Model): # "UserMixin" é responsável por armazenar métodos, funcionalidades e demais elementos necessários por que essa classe (usuario) seja reconhecida 
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30), unique=True)
    senha = db.Column(db.String())