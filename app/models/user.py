from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.username = user_dict['username']
        self.email = user_dict['email']
        self.contributions = user_dict.get('contributions', 0)
    def get_id(self):
        return str(self.id)