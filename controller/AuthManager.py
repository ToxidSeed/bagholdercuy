from flask import session


class AuthManager:
    def __init__(self):
        pass

    def get_user_information(self):
        user = {
            "user_id":session.get("user_id")
        }

        return user