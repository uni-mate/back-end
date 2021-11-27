from functools import wraps
from flask import Blueprint, request, jsonify, Response, g
import jwt


def create_chat_blueprint(services):
    chat_service = services.chat_service
    auth_service = services.auth_service
    
    chat_bp = Blueprint("chat", __name__, url_prefix="/chat")
    
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
    
    @chat_bp.route("/", methods=["GET"])
    def get_chat_rooms():
        return chat_service.get_chat_rooms()
    
    @chat_bp.route("/new-chat", methods=["POST"])
    def create_chat():
        chat_info = request.json
        chat_service.insert_new_chat(chat_info)
        return jsonify({"message": "새로운 채팅방이 만들어졌습니다."})
    
    # @chat_bp.route('/sessions')
    # def sessions():
    #     return render_template('session.html')

    # def messageReceived(methods=['GET', 'POST']):
    #     print('message was received!!!')

    # @socketio.on('my event')
    # def handle_my_custom_event(json, methods=['GET', 'POST']):
    #     print('received my event: ' + str(json))
    #     socketio.emit('my response', json, callback=messageReceived)
    
    return chat_bp
    