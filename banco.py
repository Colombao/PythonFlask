from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/AtividadeN2'
db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.String(200))

db.create_all()

# Inserir 10 mil cadastros
for _ in range(10000):
    nova_pessoa = Pessoa(nome='Nome', email='email@example.com', telefone=123456789, observacao='Observacao')
    db.session.add(nova_pessoa)
db.session.commit()

@app.route('/')
def index():
    start_time = time.time()
    resultado = Pessoa.query.limit(10000).all()
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

    return render_template('index.html', resultado=resultado, time_taken=time_taken)

if __name__ == '__main__':
    app.run(debug=True)
