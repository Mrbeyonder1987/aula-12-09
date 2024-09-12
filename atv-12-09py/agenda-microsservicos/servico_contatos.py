# servico_contatos.py
import sqlite3
from flask import Flask, request, jsonify

app_contatos = Flask(__name__)

def get_db():
    db = sqlite3.connect('contatos.db')
    db.execute('CREATE TABLE IF NOT EXISTS contatos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, telefone TEXT NOT NULL)')
    return db

@app_contatos.route('/contatos', methods=['POST'])
def adicionar_contato():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO contatos (nome, telefone) VALUES (?, ?)', (data['nome'], data['telefone']))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

@app_contatos.route('/contatos', methods=['GET'])
def listar_contatos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM contatos')
    contatos = [{'id': row[0], 'nome': row[1], 'telefone': row[2]} for row in cursor.fetchall()]
    return jsonify(contatos)

@app_contatos.route('/contatos/<int:id>', methods=['GET'])
def get_contato(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM contatos WHERE id = ?', (id,))
    row = cursor.fetchone()
    if row:
        contato = {'id': row[0], 'nome': row[1], 'telefone': row[2]}
        return jsonify(contato)
    else:
        return jsonify({'error': 'Contato não encontrado'}), 404

if __name__ == '__main__':
    app_contatos.run(port=5000)
