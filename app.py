from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)


@app.route("/clientes", methods=["POST"])
def cadastrar():
    dados = request.json

    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            clientes = json.load(arquivo)
    except:
        clientes = []

    clientes.append({
        "nome": dados["nome"],
        "telefone": dados["telefone"],
        "valor": dados["valor"]
    })

    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(clientes, arquivo, ensure_ascii=False, indent=2)

    return jsonify({"mensagem": "Salvo com sucesso!"}), 201


@app.route("/clientes", methods=["GET"])
def listar():
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            clientes = json.load(arquivo)
    except:
        clientes = []

    nomes_ruas = ["Rua das Flores", "Avenida Central", "Rua do Sol", "Praça da Matriz", "Avenida Paulista", "Rua XV de Novembro"]
    for cliente in clientes:
        cliente["endereço"] = f"{random.choice(nomes_ruas)}, {random.randint(10, 9999)}"

    return jsonify(clientes), 200


app.run(port=8080)