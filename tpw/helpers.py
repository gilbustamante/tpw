from .models import User

def find_user(user_id: int):
    """Retrieves user from database, given a user ID"""
    return User.query.filter_by(id=user_id).first()

def create_request_header(user_id: int):
    """Returns the authorization header for API requests"""
    api_key = User.query.filter_by(id=user_id).first().apikey
    config = {
        "headers": {
            "Authorization": f"Bearer {api_key}"
        }
    }
    return config