from entities import User


class Authentication:
    def __init__(self):
        self.users = []

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        raise ValueError("Invalid username or password")

    def register(self, username, password):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")

        for user in self.users:
            if user.username == username:
                raise ValueError(
                    "an account with that username already exists")

        user = User(username, password)
        self.users.append(user)
