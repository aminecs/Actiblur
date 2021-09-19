from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.ext.declarative import declarative_base

from config import settings

engine = create_engine(settings.SQLALCHEMY_URI)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()