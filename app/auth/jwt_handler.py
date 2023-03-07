"""
this file will be responsible for signing, encoding and decoding and return JWTs"
"""

import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

#functions returns the generated tokens
def token_response(token: str):
    return {
        "access_token": token,
    }

def signJWT(UserID : str):
    payload = {
        "user_id": UserID,
        "expiry": time.time() + 600
    }

    token = jwt.encode(payload , JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token : str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}