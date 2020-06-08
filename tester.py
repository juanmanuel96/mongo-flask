from mongo_flask import MongoFlask
from flask import Flask

app = Flask(__name__)
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = '27017'

mongo_db = MongoFlask(app)
mongo_db.set_Database('pyregister')
mongo_db.set_Collection('users')

for item in app.mongo_flask.collection.find():
    # print(item)
    pass

# print(current_db)

if __name__ == '__main__':
    app.run(debug=True)