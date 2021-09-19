from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from database import Base

class Users(Base): 
    __tablename__= 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, index=True)
    password_hash = Column(String(256))

    def __repr__(self): 
        return f'''Users<id={self.id}, email={self.email}
        >'''
    
    def save(self, db:Session): 
        db.session.add(self)
        db.session.commit()


class face_embedding(Base): 
    __tablename__ = 'face_embedding'

    id = Column(Integer, primary_key=True)
    embedding = Column(String(256), nullable=False)

    def __repr_(self): 
        return f'''Embedding<id={self.id}, embedding={self.embedding}>'''