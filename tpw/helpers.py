from .models import User
import requests

def find_user(user_id: int):
    """Retrieves user from database, given a user ID"""
    return User.query.filter_by(id=user_id).first()

def public_api_call(url: str):
    """Returns JSON from public endpoints"""
    return requests.get(url).json()

def auth_api_call(user_id: int, url: str):
    """Returns JSON from authenticated endpoints"""
    api_key = User.query.filter_by(id=user_id).first().apikey
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    return requests.get(url, headers=headers).json()