"""
TABLE CREATION SCRIPT

Purpose:
---------
This file is used to create database tables in MySQL based on the models defined.

What this file does:
--------------------
- Reads all models that inherit from Base
- Creates tables in the database if they do not already exist

Important:
----------
- This should be run only once (or when models change)
- If table already exists, it will NOT overwrite it

Why import Book?
----------------
Even though we don't directly use Book here,
we import it so SQLAlchemy knows about the model before creating tables.

Flow:
-----
Import models → Base.metadata → create_all() → Tables created in DB

Command to run:
---------------
python create_table.py
"""

from database import engine, Base
from model import Book

Base.metadata.create_all(bind=engine)