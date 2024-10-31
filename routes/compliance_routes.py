# routes/compliance_routes.py
from flask import Blueprint, jsonify

compliance_routes = Blueprint("compliance_routes", __name__)

@compliance_routes.route("/check", methods=["GET"])
def get_compliance_data():
    return jsonify("compliance_data")
