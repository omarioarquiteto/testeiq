from flask import Flask, request, jsonify, send_from_directory
from iqoptionapi.stable_api import IQ_Option

app = Flask(__name__)

api = None


@app.route("/")
def index():
    return send_from_directory(".", "index_novo.html")


@app.route("/login", methods=["POST"])
def login():
    global api

    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Informe e-mail e senha."
        })

    try:
        api = IQ_Option(email, password)

        status, reason = api.connect()

        if status:
            return jsonify({
                "success": True,
                "connected": api.check_connect(),
                "balance": api.get_balance()
            })

        return jsonify({
            "success": False,
            "connected": False,
            "reason": str(reason)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
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
        host="127.0.0.1",
        port=5001,
        debug=False
    )