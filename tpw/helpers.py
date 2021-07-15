from .models import User

def find_user(user_id: int):
    """Retrieves user from database, given a user ID"""
    return User.query.filter_by(id=user_id).first()