from flask import Flask, request, abort
from flask.ext.mongokit import MongoKit
from mongokit import ValidationError
from bson import ObjectId

from models import Duel
from utils import crossdomain

app = Flask(__name__)
app.config.from_object('conf')

db = MongoKit(app)
db.register([Duel, ])


@app.route('/duels', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-requested-with', 'Content-Type'])
def duels():
    if request.method == 'GET':
        try:
            limit = int(request.args.get('limit', 6))
        except ValueError:
            abort(400)
        username = request.args.get('dueler')
        if username:
            duels = db.Duel.find({"$or": [{'dueler_x': username},
                {'dueler_y': username}]}).limit(limit)
        else:
            duels = db.Duel.find().limit(limit)
        rv = app.make_response('[%s]' % ",".join(
            map(lambda x: x.to_json(), duels)))
        rv.mimetype = 'application/json'
        return rv
    else:
        try:
            json = request.form['json']
            duel = db.Duel.from_json(json)
            duel.save()
            return str(duel._id)
        except ValidationError:
            abort(400)


@app.route('/duels/<duel_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-requested-with', 'Content-Type'])
def single(duel_id):
    rv = app.make_response('%s' % db.Duel.find_one(
        {"_id": ObjectId(duel_id)}).to_json())
    rv.mimetype = 'application/json'
    return rv


if __name__ == '__main__':
    app.run()
