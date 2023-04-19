from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost:5432/pool'
db = SQLAlchemy(app)

CORS(app, resources={r"/*": {"origins": "*"}})

class Alunos(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('nome', db.String(150))
    cpf = db.Column('cpf', db.String(150))
    plano = db.Column('plano', db.String(150))

    def __init__(self, nome, cpf, plano):
        self.nome = nome
        self.cpf = cpf
        self.plano = plano

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/')
def index():
    alunos = Alunos.query.all()
    alunos_json = []
    for aluno in alunos:
        aluno_dict = {
            'id': aluno.id,
            'nome': aluno.nome,
            'cpf': aluno.cpf,
            'plano': aluno.plano
        }
        alunos_json.append(aluno_dict)

    return jsonify(alunos_json)

@app.route('/add', methods=['POST', 'OPTIONS'])
def add():
    if request.method == 'OPTIONS':
        return '', 200

    nome = request.json.get('nome')
    cpf = request.json.get('cpf')
    plano = request.json.get('plano')

    aluno = Alunos(nome=nome, cpf=cpf, plano=plano)
    db.session.add(aluno)
    db.session.commit()

    return jsonify({
        'id': aluno.id,
        'nome': aluno.nome,
        'cpf': aluno.cpf,
        'plano': aluno.plano
    }), 201

@app.route('/alunos/<int:id>', methods=['PUT'])
def edit(id):
    aluno = Alunos.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado.'}), 404
    
    nome = request.json.get('nome')
    cpf = request.json.get('cpf')
    plano = request.json.get('plano')

    if nome:
        aluno.nome = nome
    if cpf:
        aluno.cpf = cpf
    if plano:
        aluno.plano = plano
    
    db.session.commit()

    return jsonify({
        'message': 'Aluno atualizado com sucesso.',
        'aluno': {
            'id': aluno.id,
            'nome': aluno.nome,
            'cpf': aluno.cpf,
            'plano': aluno.plano
        }
    })

@app.route('/alunos/<int:id>', methods=['DELETE'])
def delete(id):
    aluno = Alunos.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado.'}), 404
    
    db.session.delete(aluno)
    db.session.commit()

    return jsonify({'message': 'Aluno deletado com sucesso.'})

if __name__ == '__main__':
    app.run(debug=True)
