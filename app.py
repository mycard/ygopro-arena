from flask import Flask, request, abort
from flask.ext.mongokit import MongoKit
from mongokit import ValidationError
from bson import ObjectId

from models import Duel

app = Flask(__name__)
app.config.from_object('conf')

db = MongoKit(app)
db.register([Duel, ])


@app.route('/duels', methods=['GET', 'POST'])
def duels():
    if request.method == 'GET':
        duels = db.Duel.find().limit(10)
        return "[%s]" % ",".join(map(lambda x: x.to_json(), duels))
    elif request.method == 'POST':
        try:
            json = request.form['json']
            duel = db.Duel.from_json(json)
            duel.save()
            return str(duel._id)
        except ValidationError:
            abort(400)


@app.route('/duels/<duel_id>')
def single(duel_id):
    return db.Duel.find_one({"_id": ObjectId(duel_id)}).to_json()


if __name__ == '__main__':
    app.run()
