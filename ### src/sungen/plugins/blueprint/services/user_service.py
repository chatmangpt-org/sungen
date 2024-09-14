class UserService:
    def get_user(self, user_id):
        # Logic to retrieve user by ID
        return {"user_id": user_id, "name": "John Doe"}

    def create_user(self, user_data):
        # Logic to create a new user
        return {"user_id": 1, "name": user_data['name']}
