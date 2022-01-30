from flask import session

class SessionManager:
    def __init__(self):
        pass

    def login(self, args={}):
        session["user_id"] = 1
