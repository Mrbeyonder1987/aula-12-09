# servico_compromissos.py
import sqlite3
from flask import Flask, request, jsonify
import requests

app_compromissos = Flask(__name__)

def get_db():
    db = sqlite3.connect('compromissos.db')
    db.execute('CREATE TABLE IF NOT EXISTS compromissos (id INTEGER PRIMARY KEY, descricao TEXT NOT NULL, data TEXT NOT NULL, contato_id INTEGER)')
    return db

@app_compromissos.route('/compromissos', methods=['POST'])
def adicionar_compromisso():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO compromissos (descricao, data, contato_id) VALUES (?, ?, ?)',
                   (data['descricao'], data['data'], data.get('contato_id')))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

@app_compromissos.route('/compromissos', methods=['GET'])
def listar_compromissos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM compromissos')
    compromissos = [{'id': row[0], 'descricao': row[1], 'data': row[2], 'contato_id': row[3]} for row in cursor.fetchall()]

    # Obter informações de contato do serviço de contatos
    for compromisso in compromissos:
        if compromisso['contato_id']:
            response = requests.get(f'http://localhost:5000/contatos/{compromisso["contato_id"]}')
            if response.status_code == 200:
                compromisso['contato'] = response.json()

    return jsonify(compromissos)

if __name__ == '__main__':
    app_compromissos.run(port=5001)
