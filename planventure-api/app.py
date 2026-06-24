from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from user_model import db, User
from auth_utils import get_current_user, require_auth, token_response
from trip_routes import bp as trip_bp
import trip_model  # ensures Trip model is registered


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(trip_bp)

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

    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json(silent=True) or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format."}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User with this email already exists."}), 409

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return token_response(user), 201

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json(silent=True) or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid email or password."}), 401

        return token_response(user), 200

    @app.route('/auth/me')
    @require_auth()
    def profile():
        user = get_current_user()
        return jsonify(user.to_dict()), 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
