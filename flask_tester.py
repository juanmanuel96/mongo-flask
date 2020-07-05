from mongo_flask import MongoFlask
from flask import Flask

app = Flask(__name__)
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DATABASE'] = 'mongo_flask'

mongo = MongoFlask(app)

print(mongo.collections)