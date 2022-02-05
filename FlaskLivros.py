# Flask

from crypt import methods
import email
from flask import Flask, jsonify, request, make_response
from estruturaBanco import Autor, Livros, app, db
import jwt
from datetime import datetime, timedelta
from functools import wraps
# Rota padrão - GET  http://localhost:5000/


def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verfificar se um token foi enviado
        if 'x-acess-token' in request.headers:
            token = request.headers['x-acess-token']
        if not token:
            return jsonify({'mensagem': 'Token não foi incluido'}, 401)
        # Se temos um token, validar acesso consultado o banco
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'])
            autor = Autor.query.filter_by(
                id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token é invalido'}, 401)
        return f(autor, *args, **kwargs)
    return decorated


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login Invalido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatorio"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow(
        ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Login Invalido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatorio"'})


@app.route('/')
@token_obrigatorio
def obter_livros(autor):
    livros = Livros.query.all()
    lista_de_livros = []
    for livro in livros:
        livro_atual = {}
        livro_atual['id_livro'] = livro.id_livro
        livro_atual['titulo'] = livro.titulo
        livro_atual['autor'] = livro.autor_livro
        livro_atual['id_autor'] = livro.id_autor
        lista_de_livros.append(livro_atual)

    return jsonify({'livros': lista_de_livros})
# Obter livro por ID - GET http://localhost:5000/livros/1


@app.route('/livros/<int:id_livro>', methods=['GET'])
@token_obrigatorio
def obter_livro_por_id(autor, id_livro):
    livro = Livros.query.filter_by(id_livro=id_livro).first()
    if not livro:
        return jsonify(f'livro não encontrado')
    livro_atual = {}
    livro_atual['titulo'] = livro.titulo
    livro_atual['autor'] = livro.autor_livro

    return jsonify({'livro': livro_atual})


# Criar um novo livro - POST http://localhost:5000/livros/


@app.route('/livros', methods=['POST'])
@token_obrigatorio
def novo_livro(autor):
    print('erro')
    novo_livro = request.get_json()
    livro = Livros(
        titulo=novo_livro['titulo'], autor_livro=novo_livro['autor'])

    db.session.add(livro)
    db.session.commit()

    return jsonify({'mensagem': 'livro adicionado com sucesso'}, 200)

# Alterar um livro existente - PUT http://localhost:5000/livros/0


@ app.route('/livros/<int:id_livro>', methods=['PUT'])
@token_obrigatorio
def alterar_livro(autor, id_livro):
    livro_a_alterar = request.get_json()
    livro = Livros.query.filter_by(id_livro=id_livro).first()
    if not livro:
        return jsonify({'Mensagem': 'Este livro nao foi encontrado'})
    try:
        if livro_a_alterar['titulo']:
            livro.titulo = livro_a_alterar['titulo']
    except:
        pass
    try:
        if livro_a_alterar['autor']:
            livro.autor = livro_a_alterar['autor']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Livro alterado com sucesso'})


# Excluir um livro - DELETE - http://localhost:5000/livros/1


@ app.route('/livros/<int:id_livro>', methods=['DELETE'])
@token_obrigatorio
def excluir_livro(autor, id_livro):
    livro_existente = Livros.query.filter_by(id_livro=id_livro).first()
    if not livro_existente:
        return jsonify({'mensagem': 'Este livro nao foi encontrado'})
    db.session.delete(livro_existente)
    db.session.commit()

    return jsonify({'mensagem': 'Livro excluido com sucesso'})


@ app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email

        lista_de_autores.append(autor_atual)

    return jsonify({'autores': lista_de_autores})


@ app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obter_autor_por_id(autor, id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'Autor não encontado')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email

    return jsonify({'autor': autor_atual})


@ app.route('/autores', methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    print('erro')
    novo_autor = request.get_json()
    autor = Autor(
        nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'])

    db.session.add(autor)
    db.session.commit()

    return jsonify({'mensagem': 'Usuario criado com sucesso'}, 200)


@ app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def alterar_autor(autor, id_autor):
    usuario_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem': 'Este usuario nao foi encontrado'})
    try:
        if usuario_a_alterar['nome']:
            autor.nome = usuario_a_alterar['nome']
    except:
        pass
    try:
        if usuario_a_alterar['email']:
            autor.email = usuario_a_alterar['email']
    except:
        pass
    try:
        if usuario_a_alterar['senha']:
            autor.senha = usuario_a_alterar['senha']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Usuario alterado com sucesso'})


@ app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor, id_autor):
    autor_existente = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_existente:
        return jsonify({'mensagem': 'Este autor nao foi encontrado'})
    db.session.delete(autor_existente)
    db.session.commit()

    return jsonify({'mensagem': 'Autor excluido com sucesso'})


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
