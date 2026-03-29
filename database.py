"""
DATABASE CONFIGURATION FILE

Purpose:
---------
This file is responsible for setting up the connection between our FastAPI app and the MySQL database.

What this file does:
--------------------
1. Creates a database connection (engine)
2. Creates a session factory (SessionLocal) to interact with DB
3. Provides a dependency (get_db) for FastAPI routes to access DB safely
4. Defines Base class which all database models will inherit from

Key Concepts:
-------------
- Engine → Main connection to the database
- Session → Used to perform DB operations (insert, read, update, delete)
- Base → Parent class for all table models
- get_db() → Ensures DB session is opened and closed properly per request

Flow:
-----
FastAPI Route → Depends(get_db) → Session created → DB operations → Session closed

Important:
----------
- Do NOT directly use engine in routes
- Always use Session (db) from get_db()
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

MYSQL_USER = "root"
MYSQL_PASSWORD = "1906"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "fastapi_db"


# mysql+pymysql://fastapi_user:FastApiPass123!@127.0.0.1:3306/fastapi_db
DATABASE_URL = F"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


# connection
engine = create_engine(DATABASE_URL)

# SESSION
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()


## BASE
Base = declarative_base()
