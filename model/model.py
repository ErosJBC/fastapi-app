from database.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    overview = Column(String(255))
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String(50))

    def model_dump(self):
        return {
            'id': self.id,
            'title': self.title,
            'overview': self.overview,
            'year': self.year,
            'rating': self.rating,
            'category': self.category
        }