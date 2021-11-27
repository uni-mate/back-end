from functools import wraps
from flask import Blueprint, json, request, jsonify, Response, g
import jwt


def create_auth_blueprint(services):
    auth_service = services.auth_service
    
    auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
    
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
    
    @auth_bp.route("/signup", methods=["POST"])
    def signup():
        new_user = request.json
        auth_service.create_new_user(new_user)
        return jsonify({"message": "회원가입 되었습니다."})
    
    # user_id 중복체크(무조건 회원가입과 다른 api로 나눠야함)
    @auth_bp.route("/signup-user-id", methods=["GET"])
    def signup_user_id():
        user_id = request.json["user_id"]
        if auth_service.check_user_id(user_id):
            return jsonify({"message": "중복된 아이디입니다."})
        else:
            return jsonify({"message": "사용할 수 있는 아이디입니다."})
    
    @auth_bp.route("/login", methods=["POST"])
    def login():
        user_info = request.json
        if auth_service.check_user_id(user_info["user_id"]):
            authorized = auth_service.login(user_info)

            if authorized:
                id = auth_service.check_id(user_info['user_id'])
                auth_service.insert_new_secret_key(id)
                secret_key = auth_service.get_secret_key(user_info['user_id'])
                token = auth_service.generate_access_token(id, secret_key)

                return jsonify({"token": token})
            else:
                return jsonify({"message": "비밀번호가 틀렸습니다."}), 403
        else:
            return jsonify({"message": "존재하지 않는 아이디 입니다."}), 404
        
    return auth_bp