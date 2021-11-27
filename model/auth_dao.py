from sqlalchemy import text


class AuthDao:
    def __init__(self, database):
        self.db = database
        
    # 회원가입 시
    def insert_user_info(self, new_user):
        return self.db.execute(text(
            """
            INSERT INTO USERS (user_id, hashed_password, email, school_email, nick_name, user_name, birth_date, gender, age, school, department, grade, self_description, registration_date, first_mbti, second_mbti, third_mbti, fourth_mbti)
            VALUES (:user_id, :password, :email, :school_email, :nick_name, :user_name, :birth_date, :gender, :age, :school, :department, :grade, :self_description, :registration_date, :first_mbti, :second_mbti, :third_mbti, :fourth_mbti)
            """
            ), new_user)
        
    def insert_interests(self, user_id, user_interest):
        return self.db.execute(text(
            """
            INSERT INTO USER_INTEREST (user_pk_id, interest_name)
            VALUES (
                (SELECT id FROM USERS
                WHERE user_id=:user_id), :user_interest
            )
            """
        ), {'user_id': user_id, 'user_interest': user_interest})
        
    def get_user_id(self, user_id):
        return self.db.execute(text(
            """
            SELECT user_id FROM USERS
            WHERE user_id=:user_id
            """
        ), {'user_id': user_id}).fetchone()
        
    def get_password(self, user_id):
        return self.db.execute(text(
            """
            SELECT hashed_password FROM USERS
            WHERE user_id=:user_id
            """
        ), {'user_id': user_id}).fetchone()
        
    def get_id(self, user_id):
        return self.db.execute(text(
            """
            SELECT id FROM USERS
            WHERE user_id=:user_id
            """
        ), {'user_id': user_id}).fetchone()
        
    def insert_new_secret_key(self, id, secret_key):
        return self.db.execute(text(
            """
            UPDATE USERS SET secret_key = ":secret_key"
            WHERE id=:id
            """
        ), {'id': id, 'secret_key': secret_key})
        
    def get_secret_key(self, user_id):
        return self.db.execute(text(
            """
            SELECT secret_key FROM USERS
            WHERE user_id=:user_id
            """
        ), {'user_id': user_id}).fetchone()