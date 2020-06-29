from mongo_flask import MongoFlask
from flask import Flask

app = Flask(__name__)
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = '27017'

mongo = MongoFlask(app)
mongo.set_Database('mongo_flask')
mongo.insert_Collection('testing')

print(mongo.get_Collection('testing'))

app.run(debug=True)