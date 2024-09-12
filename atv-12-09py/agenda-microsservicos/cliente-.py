# cliente.py
import requests

def adicionar_contato():
    nome = input("Nome do contato: ")
    telefone = input("Telefone do contato: ")
    response = requests.post('http://localhost:5000/contatos', json={'nome': nome, 'telefone': telefone})
    print(f"Contato adicionado com ID: {response.json()['id']}")

def adicionar_compromisso():
    descricao = input("Descrição do compromisso: ")
    data = input("Data do compromisso (YYYY-MM-DD HH:MM): ")
    contato_id = input("ID do contato (opcional): ")
    data = {'descricao': descricao, 'data': data}
    if contato_id:
        data['contato_id'] = int(contato_id)
    response = requests.post('http://localhost:5001/compromissos', json=data)
    print(f"Compromisso adicionado com ID: {response.json()['id']}")

def listar_contatos():
    response = requests.get('http://localhost:5000/contatos')
    contatos = response.json()
    for contato in contatos:
        print(f"ID: {contato['id']}, Nome: {contato['nome']}, Telefone: {contato['telefone']}")

def listar_compromissos():
    response = requests.get('http://localhost:5001/compromissos')
    compromissos = response.json()
    for compromisso in compromissos:
        contato = compromisso.get('contato', {})
        print(f"ID: {compromisso['id']}, Descrição: {compromisso['descricao']}, Data: {compromisso['data']}, Contato: {contato.get('nome', 'N/A')}")

def main():
    while True:
        print("\n1. Adicionar Contato")
        print("2. Adicionar Compromisso")
        print("3. Listar Contatos")
        print("4. Listar Compromissos")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_contato()
        elif opcao == '2':
            adicionar_compromisso()
        elif opcao == '3':
            listar_contatos()
        elif opcao == '4':
            listar_compromissos()
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
