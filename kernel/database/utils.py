from typing import Tuple
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from kernel.cache import CacheProxy


def get_accessor() -> Tuple[SQLAlchemy, CacheProxy]:
    core = current_app.core
    return core.db, core.cache


def paginate_query(query, start, end):
    if start != 0:
        query = query.offset(start)
    if end != -1:
        query = query.limit(end - start)
    return query
