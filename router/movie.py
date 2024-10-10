from fastapi import Path, Query, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database.database import Session
from middleware.auth import BearerJWT
from model.movie import Movie
from model.model import Movie as ModelMovie

routerMovie = APIRouter()

@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    try:
        db = Session()
        data = db.query(ModelMovie).all()
        return JSONResponse(content={'message': '¡Películas obtenidas correctamente!', 'movies': jsonable_encoder(data)})
    except Exception as e:
        return JSONResponse(content={'message': '¡Error al obtener las películas!', 'error': str(e)})

@routerMovie.get('/movies/{id}', tags=['Movies'], status_code=200)
def get_movie(id: int = Path(ge=1, le=100)):
    try:
        db = Session()
        if data := db.query(ModelMovie).filter(ModelMovie.id == id).first():
            return JSONResponse(content={'message': '¡Película obtenida correctamente!', 'movie': jsonable_encoder(data)})
        else:
            return JSONResponse(status_code=404, content={'message': '¡Película no encontrada!'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': '¡Error al obtener la película!', 'error': str(e)})

@routerMovie.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    try:
        db = Session()
        if data := db.query(ModelMovie).filter(ModelMovie.category == category.capitalize()).all():
            return JSONResponse(content={'message': '¡Películas obtenidas correctamente!', 'movies': jsonable_encoder(data)})
        else:
            return JSONResponse(status_code=404, content={'message': '¡Películas no encontradas por categoría!'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': '¡Error al obtener las películas por categoría!', 'error': str(e)})

@routerMovie.post('/movies', tags=['Movies'], status_code=201)
def create_movie(movie: Movie):
    try:
        db = Session()
        new_movie = ModelMovie(**movie.model_dump())
        db.add(new_movie)
        db.commit()
        return JSONResponse(content={'message': '¡Película creada correctamente!', 'movie': new_movie.model_dump()})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': '¡Error al crear la película!', 'error': str(e)})

@routerMovie.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: Movie):
    try:
        db = Session()
        data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
        if not data:
            return JSONResponse(status_code=404, content={'message': '¡Película no encontrada para actualizar!'})
        data.title = movie.model_dump()['title']
        data.overview = movie.model_dump()['overview']
        data.year = movie.model_dump()['year']
        data.rating = movie.model_dump()['rating']
        data.category = movie.model_dump()['category']
        db.commit()
        return JSONResponse(content={'message': '¡Película actualizada correctamente!', 'movie': data.model_dump()})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': '¡Error al actualizar la película!', 'error': str(e)})

@routerMovie.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    try:
        db = Session()
        data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
        if not data:
            return JSONResponse(status_code=404, content={'message': '¡Película no encontrada para eliminar!'})
        db.delete(data)
        db.commit()
        return JSONResponse(content={'message': '¡Película eliminada correctamente!', 'movie': data.model_dump()})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': '¡Error al eliminar la película!', 'error': str(e)})
