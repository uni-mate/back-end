class ChatService:
    def __init__(self, chat_dao):
        self.chat_dao = chat_dao
        
    def insert_new_chat(self, chat_info):
        self.chat_dao.insert_new_chat(chat_info)
        
    def get_chat_rooms(self):
        chat_info = self.chat_dao.get_chat_rooms()

        chat_result = {}
        for chat in chat_info:
                chat_result[chat[0]] = {
                    "chat_type": chat[1],
                    "meet_purpose": chat[2],
                    "title": chat[3],
                    "grade": chat[4],
                    "head_count": chat[5],
                    "gender": chat[6],
                    "description": chat[7],
                    "chat_opened_status": chat[8],
                    "common": chat[9],
                    "common_detail": chat[10],
                    "meet_status": chat[11]
                }
        return chat_result
            
        