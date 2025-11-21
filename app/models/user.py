from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.username = user_dict['username']
        self.email = user_dict['email']
        self.contributions = user_dict.get('contributions', 0)
        self.password_hashed = user_dict.get('password')
    
    def get_id(self):
        return str(self.id)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)