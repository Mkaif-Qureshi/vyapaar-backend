# app.py
from flask import Flask
from flask_cors import CORS
from config import Config
from routes.trade_routes import trade_routes
from routes.compliance_routes import compliance_routes

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Register Blueprints
app.register_blueprint(trade_routes, url_prefix="/trade")
app.register_blueprint(compliance_routes, url_prefix="/compliance")

# Simple hello route for testing
@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    app.run(debug=True)
