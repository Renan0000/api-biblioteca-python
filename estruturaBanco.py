from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

# Criar uma API flask
app = Flask(__name__)
# Criar uma instancia de SQLAlchemy
app.config['SECRET_KEY'] = 'HJADAD#@3F'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'

db = SQLAlchemy(app)
db: SQLAlchemy

# Definir a estrutura da tabela Livros
# id_livro, titulo, autor


class Livros(db.Model):
    __tablename__ = 'livros'
    id_livro = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    autor_livro = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))
# Definir a estrutura da tabela Autor
# id_autor,nome,email,senha,admin,postagens


class Autor(db.Model):
    __tablename___ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Livros')


def inicializar_banco():
    # Executar o comando para criar o banco de dados
    db.drop_all()
    db.create_all()
# Criar usuario administrador
    autor = Autor(nome='renan', email='Renanrocha6@gmail.com',
                  senha='123456', admin=True)
    db.session.add(autor)
    db.session.commit()


if __name__ == "__main__":
    inicializar_banco()
