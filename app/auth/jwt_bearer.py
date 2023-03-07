from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
    def __init__(self, auto_error : bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            print(credentials)
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="line 13")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="line 16")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="line 18")

    def verify_jwt(self, jwttoken: str):
        is_token_valid : bool = False
        payload = decodeJWT(jwttoken)
        if payload:
            is_token_valid = True
        return is_token_valid