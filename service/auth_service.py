import string, secrets
from datetime import date

import jwt
import bcrypt


class AuthService:
    def __init__(self, auth_dao):
        self.auth_dao = auth_dao
        
    def create_new_user(self, new_user):
        new_user["password"] = bcrypt.hashpw(
            new_user["password"].encode("UTF-8"), bcrypt.gensalt()
        )
        new_user["password"] = new_user["password"].decode("utf-8")
        
        new_user["registration_date"] = date.today().isoformat()
        
        self.auth_dao.insert_user_info(new_user)
        for user_interest in new_user["interests"]:
            self.auth_dao.insert_interests(new_user["user_id"], user_interest)
        
    def check_user_id(self, user_id):
        if self.auth_dao.get_user_id(user_id):
            return user_id
        else:
            return None
        
    def login(self, user_info):
        user_id = user_info["user_id"]
        password = user_info["password"]
        user_password = self.auth_dao.get_password(user_id)

        authorized = user_password["hashed_password"] and bcrypt.checkpw(
            password.encode("UTF-8"), user_password["hashed_password"].encode("UTF-8")
        )
        return authorized
    
    def check_id(self, user_id):
        id = self.auth_dao.get_id(user_id)
        return id["id"]
    
    def insert_new_secret_key(self, id):
        string_pool = string.ascii_letters + string.digits
        while True:
            secret_key = "".join(secrets.choice(string_pool) for _ in range(10))
            if (
                any(c.islower() for c in secret_key)
                and any(c.isupper() for c in secret_key)
                and sum(c.isdigit() for c in secret_key) >= 3
            ):
                break
        self.auth_dao.insert_new_secret_key(id, secret_key)
        
    def get_secret_key(self, user_id):
        user_secret_key = self.auth_dao.get_secret_key(user_id)
        if user_secret_key is None:
            return None
        return user_secret_key["secret_key"]
    
    def generate_access_token(self, id, secret_key):
        payload = {"id": id}
        token = jwt.encode(payload, secret_key, "HS256")
        return token