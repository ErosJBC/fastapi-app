from fastapi import APIRouter
from fastapi.responses import JSONResponse
from model.user import User
from jwt_app import createToken

routerUser = APIRouter()

@routerUser.post('/login', tags=['Authentication'])
def login(user: User):
    if user.email == 'erosjbc@gmail.com' and user.password == '12345':
        token: str = createToken(user.model_dump())
        return JSONResponse(content={'message': '¡Inicio de sesión correcto!', 'token': token})
