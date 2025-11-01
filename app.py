from flask import Flask, request, jsonify
from verifica_senha import verificar_senha

app = Flask(__name__)

@app.route("/")
def home():
    return {"mensagem": "API de verificação de senha funcionando!"}

@app.route("/verificar", methods=["POST"])
def verificar():
    dados = request.get_json()
    senha = dados.get("senha", "")
    resultado = verificar_senha(senha)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
