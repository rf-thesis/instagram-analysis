# create table for the search 
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db_url
DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(db_url)


def create_db_session(engine):
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    return session


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class Insta(DeclarativeBase):
    __tablename__ = "instagram"

    media_id = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    predicted_gender = Column(String, nullable=True)
    created_time = Column(DateTime, nullable=True)
    like_count = Column(BigInteger, nullable=True)
    comment_count = Column(BigInteger, nullable=True)
    media_text = Column(String, nullable=True)
    hashtags = Column(ARRAY(String), nullable=True)
    photo_url = Column(String, nullable=True)
    location_name = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    location_id = Column(BigInteger, nullable=True)
    country = Column(String, nullable=True)
    n_faces = Column(Integer, nullable=True)
