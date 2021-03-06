from .auth_view import create_auth_blueprint
from .chat_view import create_chat_blueprint
from .user_view import create_user_blueprint


def create_endpoints(app, services):
    @app.route("/ping", methods=["GET"])
    def ping():
        return "pong"

    app.register_blueprint(create_auth_blueprint(services))
    app.register_blueprint(create_chat_blueprint(services))
    app.register_blueprint(create_user_blueprint(services))