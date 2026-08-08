from flask import Flask, request, jsonify
import json

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
        "endereco": dados["endereco"],
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

    return jsonify(clientes), 200


app.run(port=8080)