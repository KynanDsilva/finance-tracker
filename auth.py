class User:
    users = []
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        User.users.append(self)
    @staticmethod
    def authenticate(username, password):
        for user in User.users:
            if user.username == username and user.password == password:
                return True
        