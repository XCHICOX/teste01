from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Caminhos para arquivos de dados
DATA_FOLDER = 'data'

def load_data(filename):
    try:
        with open(os.path.join(DATA_FOLDER, filename), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(filename, data):
    with open(os.path.join(DATA_FOLDER, filename), 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuarios = load_data('usuarios.json')
        
        # Verifica se o usuário e senha são válidos
        for usuario in usuarios:
            if usuario['username'] == username and usuario['password'] == password:
                session['username'] = username
                return redirect(url_for('home'))
                
        # Se a autenticação falhar
        return render_template('login.html', error='Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Função para verificar se o usuário está logado e passar o nome de usuário para os templates
def get_logged_in_user():
    return session.get('username', None)

# Adicionar o nome de usuário em todas as rotas que renderizam templates
@app.context_processor
def inject_logged_in_user():
    return {'logged_in_user': get_logged_in_user()}

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/clientes')
def clientes():
    if 'username' not in session:
        return redirect(url_for('index'))
    clientes = load_data('clientes.json')
    return render_template('clientes.html', clientes=clientes)

@app.route('/veiculos')
def veiculos():
    if 'username' not in session:
        return redirect(url_for('index'))
    veiculos = load_data('veiculos.json')
    return render_template('veiculos.html', veiculos=veiculos)

@app.route('/manutencoes')
def manutencoes():
    if 'username' not in session:
        return redirect(url_for('index'))
    manutencoes = load_data('manutencoes.json')
    return render_template('manutencoes.html', manutencoes=manutencoes)

@app.route('/adicionar_cliente', methods=['POST'])
def adicionar_cliente():
    if 'username' not in session:
        return redirect(url_for('index'))
    cliente = {
        'nome': request.form['nome'],
        'rg': request.form['rg'],
        'endereco': request.form['endereco'],
        'telefone': request.form['telefone'],
        'whatsapp': request.form['whatsapp'],
        'usuario_cadastro': session['username']
    }
    clientes = load_data('clientes.json')
    clientes.append(cliente)
    save_data('clientes.json', clientes)
    return redirect(url_for('clientes'))

@app.route('/editar_cliente', methods=['POST'])
def editar_cliente():
    if 'username' not in session:
        return redirect(url_for('index'))
    rg = request.form['rg']
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    whatsapp = request.form['whatsapp']
    clientes = load_data('clientes.json')
    for cliente in clientes:
        if cliente['rg'] == rg:
            cliente.update({
                'nome': nome,
                'endereco': endereco,
                'telefone': telefone,
                'whatsapp': whatsapp
            })
            break
    save_data('clientes.json', clientes)
    return redirect(url_for('clientes'))

@app.route('/excluir_cliente', methods=['POST'])
def excluir_cliente():
    if 'username' not in session:
        return redirect(url_for('index'))
    rg = request.form['rg']
    clientes = load_data('clientes.json')
    clientes = [c for c in clientes if c['rg'] != rg]
    save_data('clientes.json', clientes)
    return redirect(url_for('clientes'))

@app.route('/adicionar_veiculo', methods=['POST'])
def adicionar_veiculo():
    if 'username' not in session:
        return redirect(url_for('index'))
    veiculo = {
        'placa': request.form['placa'],
        'modelo': request.form['modelo'],
        'ano': request.form['ano'],
        'usuario_cadastro': session['username']
    }
    veiculos = load_data('veiculos.json')
    veiculos.append(veiculo)
    save_data('veiculos.json', veiculos)
    return redirect(url_for('veiculos'))

@app.route('/editar_veiculo', methods=['POST'])
def editar_veiculo():
    if 'username' not in session:
        return redirect(url_for('index'))
    placa = request.form['placa']
    modelo = request.form['modelo']
    ano = request.form['ano']
    veiculos = load_data('veiculos.json')
    for veiculo in veiculos:
        if veiculo['placa'] == placa:
            veiculo.update({
                'modelo': modelo,
                'ano': ano
            })
            break
    save_data('veiculos.json', veiculos)
    return redirect(url_for('veiculos'))

@app.route('/excluir_veiculo', methods=['POST'])
def excluir_veiculo():
    if 'username' not in session:
        return redirect(url_for('index'))
    placa = request.form['placa']
    veiculos = load_data('veiculos.json')
    veiculos = [v for v in veiculos if v['placa'] != placa]
    save_data('veiculos.json', veiculos)
    return redirect(url_for('veiculos'))

@app.route('/adicionar_manutencao', methods=['POST'])
def adicionar_manutencao():
    if 'username' not in session:
        return redirect(url_for('index'))
    manutencao = {
        'data': request.form['data'],
        'placa': request.form['placa'],
        'informacoes': request.form['informacoes'],
        'mecanico': request.form['mecanico'],
        'valor': request.form['valor'],
        'usuario_cadastro': session['username']
    }
    manutencoes = load_data('manutencoes.json')
    manutencoes.append(manutencao)
    save_data('manutencoes.json', manutencoes)
    return redirect(url_for('manutencoes'))

@app.route('/editar_manutencao', methods=['POST'])
def editar_manutencao():
    if 'username' not in session:
        return redirect(url_for('index'))
    # Similar to adicionar_manutencao but for editing
    pass

@app.route('/excluir_manutencao', methods=['POST'])
def excluir_manutencao():
    if 'username' not in session:
        return redirect(url_for('index'))
    # Similar to adicionar_manutencao but for deleting
    pass

if __name__ == '__main__':
    app.run(debug=True)
