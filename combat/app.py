import simplejson

from bson import ObjectId
from datetime import datetime
from flask import Flask, request, abort, jsonify
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
    elif request.method == 'POST':
        try:
            json = request.form['json']
            duel = db.Duel.from_json(json)
            deckreco = DeckReco()
            deck_x_slug = deckreco.parse_ids(duel.deck_x['main']).slug
            deck_y_slug = deckreco.parse_ids(duel.deck_y['main']).slug
            deck_x = db.Deck.find_one({"slug": deck_x_slug})
            if deck_x_slug == deck_y_slug:
                deck_y = deck_x
            else:
                deck_y = db.Deck.find_one({"slug": deck_y_slug})
            deck_x.count += 1
            deck_y.count += 1
            if duel.winner:
                deck_x.win_count += 1
                deck_y.lose_count += 1
                deck_x.save()
                deck_y.save()
                duel['credit_x'] = get_winner_credit(deck_x)
                duel['credit_y'] = get_loser_credit(deck_y)
            else:
                deck_x.lose_count += 1
                deck_y.win_count += 1
                deck_x.save()
                deck_y.save()
                duel['credit_x'] = get_loser_credit(deck_x)
                duel['credit_y'] = get_winner_credit(deck_y)
            duel.save()
            json = simplejson.dumps({'credit_x': duel.credit_x,
                'credit_y': duel.credit_y, 'duel_id': str(duel._id)})
            rv = app.make_response(json)
        except ValidationError:
            abort(400)
    rv.mimetype = 'application/json'
    return rv


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
