""" src/constants.py
    This module loads all the variables from the environment.
"""
from dotenv import load_dotenv
import os
load_dotenv()


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")