from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost:5432/pool'
db = SQLAlchemy(app)

class Alunos(db.Model):
    id = db.Column('id', db.Integer, primary_key = True,autoincrement=True)
    nome= db.Column('nome', db.String(150))
    cpf= db.Column('cpf', db.String(150))
    plano= db.Column('plano', db.String(150))

    def __init__(self,nome, cpf, plano):
        self.nome =nome
        self.cpf=cpf
        self.plano=plano
    
                  

@app.route('/')
def index():
    alunos = Alunos.query.all()
    return render_template("index.html", alunos = alunos)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        alunos = Alunos(
            request.form['nome'],
            request.form['cpf'],
            request.form['plano'])
        
        db.session.add(alunos)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', nome='nome', cpf='cpf', plano='plano')

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    alunos = Alunos.query.get(id)
    if request.method =='POST':
        alunos.nome= request.form['nome'],
        alunos.cpf=request.form['cpf'],
        alunos.plano=request.form['plano']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', alunos = alunos)

@app.route('/delete/<int:id>')
def delete(id):
    alunos = Alunos.query.get(id)
    db.session.delete(alunos)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)