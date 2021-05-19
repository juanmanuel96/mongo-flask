from mongo_flask import MongoFlask
from flask import Flask

from mongo_flask.core.collections import CollectionModel
from mongo_flask.core.fields import StringField

app = Flask(__name__)
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DATABASE'] = 'mongo_flask'

mongo = MongoFlask(app)


class Testing(CollectionModel):
    collection_name = None
    doc_num = StringField()
    desc = StringField()


mongo.register_collection(Testing)
collection = mongo.get_collection('testing2')

doc_found = collection.get()
print(doc_found)
