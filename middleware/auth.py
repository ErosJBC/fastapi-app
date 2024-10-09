from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jwt_app import validateToken

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        if auth and auth.credentials:
            data = validateToken(auth.credentials)
        else:
            raise HTTPException(status_code=403, detail='Invalid authentication credentials')
        if data['email'] != 'erosjbc@gmail.com':
            raise HTTPException(status_code=403, detail='Invalid user credentials')
