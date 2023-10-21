from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import time
import random
import string

app = Flask(__name__)

# Configurando o SQLAlchemy para usar o pymysql como conector MySQL
pymysql.install_as_MySQLdb()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/testedb'
db = SQLAlchemy(app)

# Defina o modelo para o banco de dados
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    observacao = db.Column(db.String(20), nullable=False)

# Crie um contexto de aplicação para operações de banco de dados
with app.app_context():
    # Crie as tabelas do banco de dados
    db.create_all()

    # Adicione 10.000 registros à tabela Pessoa
    for _ in range(10000):
        nome = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))  # Gera um nome aleatório
        email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@example.com'  # Gera um email aleatório
        telefone = ''.join(random.choices(string.digits, k=9))  # Gera um número de telefone aleatório
        observacao = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))  # Gera uma observação aleatória

        nova_pessoa = Pessoa(nome=nome, email=email, telefone=telefone, observacao=observacao)
        db.session.add(nova_pessoa)

    # Faça o commit das alterações no banco de dados
    db.session.commit()
@app.route('/', methods=['POST'])
def adicionar_pessoa():


    return jsonify({'message': 'Pessoa adicionada com sucesso!'})

@app.route('/consultar', methods=['GET'])
def consultar_registros():
    # Medir o tempo de execução da consulta
    start_time = time.time()

    # Realizar a consulta para retornar 10.000 registros da tabela Pessoa
    pessoas = Pessoa.query.limit(10000).all()

    # Calcular o tempo de execução em milissegundos
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # em milissegundos

    # Criar uma lista com os resultados para retorno
    resultados = []
    for pessoa in pessoas:
        resultados.append({
            'id': pessoa.id,
            'nome': pessoa.nome,
            'email': pessoa.email,
            'telefone': pessoa.telefone,
            'observacao': pessoa.observacao
        })

    # Retornar os resultados e o tempo de execução em milissegundos
    return jsonify({'tempo_execucao_ms': execution_time, 'resultados': resultados})

@app.route('/', methods=['GET'])  # Defina uma rota para a função index
def index():
    # Simulando dados da consulta para o exemplo
    start_time = time.time()
    pessoas = Pessoa.query.limit(10000).all()  # obtendo 100000 registros do banco de dados

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # em milissegundos
    # Renderizando o template com os dados
    return render_template('resultado.html', tempo_execucao=execution_time, pessoas=pessoas)


if __name__ == '__main__':
    app.run(debug=True)
