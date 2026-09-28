from flask import Flask, request, jsonify, send_from_directory
from iqoptionapi.stable_api import IQ_Option
import os
import sys
import time
import traceback
import iqoptionapi
import websocket

app = Flask(__name__)

api = None


@app.route("/")
def index():
    return send_from_directory(".", "index_novo.html")


@app.route("/login", methods=["POST"])
def login():
    global api

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Informe e-mail e senha."
        })

    started = time.time()

    try:
        print("======================================")
        print("INICIANDO TESTE DE CONEXAO IQ OPTION")
        print(f"Python: {sys.version}")
        print(f"iqoptionapi: {getattr(iqoptionapi, '__version__', 'desconhecida')}")
        print(f"websocket-client: {getattr(websocket, '__version__', 'desconhecida')}")
        print("Criando objeto IQ_Option...")

        api = IQ_Option(email, password)

        print("Executando api.connect()...")
        status, reason = api.connect()

        elapsed = round(time.time() - started, 2)

        print(f"connect() terminou em {elapsed}s")
        print(f"Status: {status}")
        print(f"Reason type: {type(reason).__name__}")
        print(f"Reason: {reason}")

        if status:
            connected = api.check_connect()
            balance = api.get_balance()

            print(f"check_connect(): {connected}")
            print("Conexao realizada com sucesso.")
            print("======================================")

            return jsonify({
                "success": True,
                "connected": connected,
                "balance": balance,
                "elapsed_seconds": elapsed,
                "python": sys.version.split()[0],
                "iqoptionapi": getattr(iqoptionapi, "__version__", "desconhecida"),
                "websocket_client": getattr(websocket, "__version__", "desconhecida")
            })

        print("Conexao recusada pela API.")
        print("======================================")

        return jsonify({
            "success": False,
            "connected": False,
            "reason": str(reason),
            "reason_type": type(reason).__name__,
            "elapsed_seconds": elapsed,
            "python": sys.version.split()[0],
            "iqoptionapi": getattr(iqoptionapi, "__version__", "desconhecida"),
            "websocket_client": getattr(websocket, "__version__", "desconhecida")
        })

    except Exception as e:
        elapsed = round(time.time() - started, 2)
        error_type = type(e).__name__
        error_message = str(e)
        error_traceback = traceback.format_exc()

        print("======================================")
        print("ERRO DURANTE api.connect()")
        print(f"Tempo: {elapsed}s")
        print(f"Tipo: {error_type}")
        print(f"Mensagem: {error_message}")
        print("Traceback:")
        print(error_traceback)
        print("======================================")

        return jsonify({
            "success": False,
            "error": error_message,
            "error_type": error_type,
            "elapsed_seconds": elapsed,
            "python": sys.version.split()[0],
            "iqoptionapi": getattr(iqoptionapi, "__version__", "desconhecida"),
            "websocket_client": getattr(websocket, "__version__", "desconhecida"),
            "traceback": error_traceback
        })


if __name__ == "__main__":
    print("")
    print("======================================")
    print("       TESTE IQ OPTION - NOVO")
    print("======================================")
    print("")
    print("Abra:")
    print("http://127.0.0.1:5001")
    print("")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5001)),
        debug=False
    )
