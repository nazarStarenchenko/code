from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a base class for the models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

# Create an SQLite engine and session
engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)

# Create the tables
Base.metadata.create_all(engine)
