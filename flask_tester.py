from mongo_flask import MongoFlask
from flask import Flask

app = Flask(__name__)
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DATABASE'] = 'mongo_flask'

mongo = MongoFlask(app)

col = mongo.get_collection('testing')
docs = col.list_find()

with mongo.start_session() as session:
    one_doc = col.find_one(doc_num='doc0', session=session)
    print(one_doc)

