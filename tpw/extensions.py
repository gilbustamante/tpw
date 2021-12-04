from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

db = SQLAlchemy()

cache_config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(config=cache_config)
