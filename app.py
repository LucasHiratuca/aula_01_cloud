from flask import Flask, request, jsonify, render_template, redirect, url_for
import random
import mysql.connector
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS (MYSQL)
# ==========================================
def get_db_connection():
    # Busca as configurações seguras que estão no arquivo .env
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def get_clientes():
    """
    Função auxiliar que busca os dados no MySQL
    """
    try:
        conn = get_db_connection()
        # dictionary=True faz com que os dados voltem em formato de dicionário (json-like)
        cursor = conn.cursor(dictionary=True) 
        
        cursor.execute("SELECT nome, telefone, valor FROM clientes")
        clientes = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")
        clientes = []

    # Mantendo a nossa lógica antiga do campo gerado na hora:
    nomes_ruas = ["Rua das Flores", "Avenida Central", "Rua do Sol", "Praça da Matriz", "Avenida Paulista", "Rua XV de Novembro"]
    for cliente in clientes:
        cliente["endereço"] = f"{random.choice(nomes_ruas)}, {random.randint(10, 9999)}"

    return clientes


# ==========================================
# ROTAS DA APLICAÇÃO
# ==========================================

@app.route("/", methods=["GET"])
def index():
    clientes = get_clientes()
    return render_template("index.html", clientes=clientes)


@app.route("/clientes", methods=["GET"])
def listar():
    clientes = get_clientes()
    return jsonify(clientes), 200


@app.route("/clientes", methods=["POST"])
def cadastrar():
    is_api_request = request.is_json
    dados = request.json if is_api_request else request.form

    nome = dados.get("nome")
    telefone = dados.get("telefone")
    valor = dados.get("valor")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # O %s previne SQL Injection (protege o banco contra dados maliciosos)
        sql = "INSERT INTO clientes (nome, telefone, valor) VALUES (%s, %s, %s)"
        valores = (nome, telefone, valor)
        
        cursor.execute(sql, valores)
        conn.commit() # Efetiva a gravação no banco
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")
        if is_api_request:
            return jsonify({"erro": str(e)}), 500
        else:
            return "Erro ao salvar no banco. Verifique o console.", 500

    if is_api_request:
        return jsonify({"mensagem": "Salvo com sucesso no MySQL!"}), 201
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)