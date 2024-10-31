# routes/trade_routes.py
from flask import Blueprint, jsonify, request

trade_routes = Blueprint("trade_routes", __name__)

@trade_routes.route("/requirements", methods=["GET"])
def get_trade_requirements():
    market = request.args.get("market", "US")
    return jsonify("requirements")
