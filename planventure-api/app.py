from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from user_model import db, User
import trip_model  # ensures Trip model is registered


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to PlanVenture API"})

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"})

    @app.route('/users')
    def list_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
