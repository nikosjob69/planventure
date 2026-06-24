try:
    from flask import jsonify  # type: ignore[import]
except Exception:  # pragma: no cover - fallback for environments without Flask
    def jsonify(obj):
        """Fallback jsonify for environments where Flask isn't installed.
        Returns the object unchanged (useful for type checking / linting).
        """
        return obj

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request  # type: ignore[import]
from user_model import User


def create_token(user):
    return create_access_token(identity=str(user.id))


def get_current_user(optional: bool = False):
    """Return the current authenticated user from JWT identity.

    If optional is True, this function will allow unauthenticated requests and
    return None when no JWT is present.
    """
    verify_jwt_in_request(optional=optional)
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


def require_auth():
    """Decorator for protecting routes with JWT authentication."""
    return jwt_required()


def token_response(user):
    return jsonify({
        "access_token": create_token(user),
        "user": user.to_dict()
    })
