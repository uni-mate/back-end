from sqlalchemy import text

class ChatDao:
    def __init__(self, database):
        self.db = database
        
    def insert_new_chat(self, chat_info):
        return self.db.execute(text(
            """
            INSERT INTO CHATS (chat_type, meet_purpose, title, grade, head_count, gender, description, common, common_detail)
            VALUES (:chat_type, :meet_purpose, :title, :grade, :head_count, :gender, :description, :common, :common_detail)
            """
        ), chat_info)
        
    def get_chat_rooms(self):
        return self.db.execute(text(
            """
            SELECT id, chat_type, meet_purpose, title, grade, head_count, gender, description, chat_opened_status, common, common_detail, meet_status
            FROM CHATS
            """
        )).fetchall()