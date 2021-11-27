from sqlalchemy import text

class UserDao:
    def __init__(self, database):
        self.db = database