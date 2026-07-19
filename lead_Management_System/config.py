import os

class Config:
    SECRET_KEY = "leadmanagement123"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DATABASE = os.path.join(BASE_DIR, "database.db")