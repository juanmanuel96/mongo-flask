from .mongo_flask import MongoFlask
from .mongo_flask.wrappers import MongoClient, MongoCollection, MongoDatabase
from flask import Flask

app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
mongo = MongoFlask(app)

def test_db_connection():
    assert type(app.mongo) == type(MongoFlask())