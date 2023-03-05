from base64 import decode
from calendar import c
from enum import auto
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_Error=auto_Error)

    async def __call__(self, request: Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.schema == "Bearer":
                raise HTTPException(status_code=403, details="Invalid or Expired token")
            return credentials.credentials

        else:
            raise HTTPException(status_code=403, details="Invalid or Expired token")

    def verify_jwt(self, jwttoken: str):
        is_token_valid : bool = False
        payload = decodeJWT(jwttoken)
        if payload:
            is_token_valid = True
        return is_token_valid