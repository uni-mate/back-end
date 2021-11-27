import os

from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv

from model import AuthDao, ChatDao, UserDao
from service import AuthService, ChatService, UserService
from view import create_endpoints


class Sercices:
    pass

def create_app(test_config=None):
    load_dotenv()
    
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_envvar("APP_SETTINGS")
    else:
        app.config.update(test_config)
    
    database = create_engine(app.config["DB_URL"], encoding="utf-8", max_overflow=0)

    # Persistence 레이어
    auth_dao = AuthDao(database)
    chat_dao = ChatDao(database)
    user_dao = UserDao(database)
    
    # Business 레이어
    services = Sercices
    services.auth_service = AuthService(auth_dao)
    services.chat_service = ChatService(chat_dao)
    services.user_service = UserService(user_dao)
    
    # Presentation 레이어
    create_endpoints(app, services)
    
    return app