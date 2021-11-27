from functools import wraps
from flask import Blueprint, request, jsonify, Response, g
import jwt


def create_user_blueprint(services):
    user_service = services.user_service
    auth_service = services.auth_service

    user_bp = Blueprint("user", __name__, url_prefix="/user")

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = request.headers.get("Authorization")
            if access_token:
                access_token = access_token.replace("Bearer ", "")
                try:
                    payload = jwt.decode(
                        access_token,
                        algorithms="HS256",
                        options={"verify_signature": False},
                    )
                except jwt.DecodeError:
                    return Response(status=401)
                user_id = payload["user_id"]
                user_secret_key = auth_service.get_secret_key(user_id)
                try:
                    payload = jwt.decode(access_token, user_secret_key, "HS256")
                except jwt.InvalidTokenError:
                    return Response(status=401)
                g.user_id = user_id
            else:
                return Response(status=401)
            return f(*args, **kwargs)

        return decorated_function
    
    @user_bp.route("/", methods=["GET"])
    def get_user_info():
        pass
    
    return user_bp