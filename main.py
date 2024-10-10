import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from database.database import Base, engine
from router.movie import routerMovie
from router.user import routerUser

app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Esta es una API de prueba para aprender FastAPI',
    version='0.0.1',
)

app.include_router(routerUser)
app.include_router(routerMovie)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo! Este es un curso de FastAPI.</h2>')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("main:app", host='127.0.0.1', port=port)
