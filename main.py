from fastapi import FastAPI, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from models.movie import Movie
from models.user import User
from data.movies import movies
from jwt_app import createToken
from middleware.auth import BearerJWT

app = FastAPI(
    title='Aprendiendo FastAPI',
    description='Esta es una API de prueba para aprender FastAPI',
    version='0.0.1',
)

@app.post('/login', tags=['Authentication'])
def login(user: User):
    if user.email == 'erosjbc@gmail.com' and user.password == '12345':
        token: str = createToken(user.model_dump())
        return JSONResponse(content={'message': '¡Inicio de sesión correcto!', 'token': token})

@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo!</h2>')

@app.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['Movies'], status_code=200)
def get_movie_by_id(id: int = Path(ge=1, le=100)):
    return next((movie for movie in movies if movie["id"] == id), {})

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    return next((movie for movie in movies if str(movie["category"]).lower() == category.lower()), {})

@app.post('/movies/', tags=['Movies'])
def create_movie(movie: Movie):
    movies.append(movie.model_dump())
    return JSONResponse(content={'message': '¡Película creada correctamente!', 'movie': movie.model_dump()})

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["category"] = movie.category
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            return JSONResponse(content={'message': '¡Película actualizada correctamente!', 'movie': item})
    return JSONResponse(content={'message': '¡Película no encontrada!', 'movies': movies})

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={'message': '¡Película eliminada correctamente!', 'movies': movies})
    return JSONResponse(content={'message': '¡Película no encontrada!', 'movies': movies})