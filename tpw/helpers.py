from .models import User
import requests

def find_user(user_id: int):
    """Retrieves user from database, given a user ID"""
    return User.query.filter_by(id=user_id).first()

def auth_api_call(user_id: int, url: str):
    """Returns JSON from call to GW2's API with provided endpoint"""
    api_key = User.query.filter_by(id=user_id).first().apikey
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    req = requests.get(url, headers=headers).json()
    return req