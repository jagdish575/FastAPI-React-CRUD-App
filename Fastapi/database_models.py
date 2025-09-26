from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = Session(bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    quantity = Column(Integer)


# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency to get the DB session for each request
def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()
