import os

from neo4j.exceptions import SessionExpired
from neomodel import db


def handle_neo4j_session_timeout(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SessionExpired:
            db.set_connection(os.environ["NEO4J_CONNECTION_URI"])
            func(*args, **kwargs)

    return inner
