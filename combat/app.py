from bson import ObjectId
from datetime import datetime
from flask import Flask, request, abort
from flask.ext.mongokit import MongoKit
from mongokit import ValidationError

from combat.deck import DeckReco, FakeDeckRule
from combat.models import Duel, Deck
from combat.utils import crossdomain

app = Flask(__name__)
app.config.from_object('combat.conf')

db = MongoKit(app)
db.register([Duel, Deck, ])

from combat.ranking import get_winner_credit, get_loser_credit


@app.route('/test')
def test():
    test = db.decks.aggregate({"$group": {"_id": None,
                                          "total_win": {"$sum": "$win_count"},
                                          "total_lose": {"$sum": "$lose_count"}
                                          }})['result']
    return unicode(test)


@app.route('/duels', methods=['GET', 'POST'])
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
    elif request.method == 'POST':
        try:
            json = request.form['json']
            duel = db.Duel.from_json(json)
            if duel.winner:
                duel.credit_x = get_winner_credit(duel.deck_x['main'])
                duel.credit_y = get_loser_credit(duel.deck_y['main'])
            else:
                duel.credit_x = get_loser_credit(duel.deck_x['main'])
                duel.credit_y = get_winner_credit(duel.deck_y['main'])
            duel.save()
            return str(duel._id)
        except ValidationError:
            abort(400)


@app.route('/duels/<duel_id>', methods=['GET'])
@crossdomain(origin='*', headers=['x-requested-with', 'Content-Type'])
def single(duel_id):
    rv = app.make_response('%s' % db.Duel.find_one(
        {"_id": ObjectId(duel_id)}).to_json())
    rv.mimetype = 'application/json'
    return rv


@app.route('/updatedecks', methods=['GET'])
def update_decks():
    deckreco = DeckReco()
    rules = deckreco.rules + [FakeDeckRule(), ]
    _decks_in_rule = set([rule.slug for rule in rules])
    _decks_in_db = set([deck.slug for deck in db.Deck.find()])
    _decks_to_add = _decks_in_rule - _decks_in_db
    _decks_to_del = _decks_in_db - _decks_in_rule
    decks_to_add = [rule for rule in rules if rule.slug
                    in _decks_to_add]
    decks_to_del = [db.Deck.find_one({"slug": slug}) for slug
                    in _decks_to_del]

    for d in decks_to_add:
        deck = db.Deck()
        deck.slug = unicode(d.slug)
        deck.trans = d.trans
        deck.save()

    for d in decks_to_del:
        d.delete()

    deck_amount = db.decks.count()
    return '%d decks added, %d decks deleted, total %d decks.' % (
        len(decks_to_add), len(decks_to_del), deck_amount)
