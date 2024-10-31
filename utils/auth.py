# utils/auth.py
import jwt
from config import Config

def validate_token(token):
    try:
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.InvalidTokenError:
        return None
