# -*- coding: utf-8 -*-
import re
import simplejson

from bson import Code
from bson.objectid import ObjectId
from flask import Flask, request, abort, jsonify
from flask.ext.mongokit import MongoKit
from mongokit import ValidationError

from combat.conf import QUERY_LIMIT, OUTPUT_ROUND
from combat.deck import DeckReco, FakeDeckRule
from combat.models import Duel, Deck, User
from combat.utils import crossdomain, json_response
from combat.ranking import elo_add, rank

app = Flask(__name__)
app.config.from_object('combat.conf')

db = MongoKit(app)
db.register([Duel, Deck, User])

update_ranking = """
var rank = 0;
var prev = 0;
db.%(c)s.find().sort({rating: -1}).forEach(function(s){
    if (prev != s.rating){
        rank++;
    }
    db.%(c)s.update({_id:s._id}, {$set: {ranking: NumberInt(rank)}});
    prev = s.rating;
})
"""


def get_user(username):
    user = db.User.find_one({"username": username})
    if not user and username:
        user = db.User()
        if re.match(r"[a-zA-Z0-9]\w+", username):
            user.username = username
            user.save()
        else:
            abort(400)
    return user


def user_to_json(user):
    return simplejson.dumps({
        "losses": user.losses,
        "rank": rank(user),
        "ranking": user.ranking,
        "rating": round(user.rating, OUTPUT_ROUND),
        "total": user.total,
        "username": user.username,
        "wins": user.wins,
    })


def deck_to_json(deck):
    return simplejson.dumps({
        "losses": deck.losses,
        "rank": rank(deck),
        "ranking": deck.ranking,
        "rating": round(deck.rating, OUTPUT_ROUND),
        "slug": deck.slug,
        "total": deck.total,
        "trans": deck.trans,
        "wins": deck.wins,
    })


@app.route('/duels', methods=['GET', 'POST'])
@crossdomain(origin='*')
@json_response
def duels():
    if request.method == 'GET':
        try:
            limit = int(request.args.get('limit', QUERY_LIMIT))
        except ValueError:
            abort(400)
        duels = db.Duel.find().limit(limit)
        json = '{"duels": [%s]}' % ",".join(map(lambda x: x.to_json(), duels))
    elif request.method == 'POST':
        try:
            json = request.form['json']
            duel = db.Duel.from_json(json)
            # recognize decks
            deckreco = DeckReco()
            recognized_x = deckreco.parse_ids(duel.deck_x['main'])
            recognized_y = deckreco.parse_ids(duel.deck_y['main'])
            duel.deck_x['slug'] = unicode(recognized_x.slug)
            duel.deck_y['slug'] = unicode(recognized_y.slug)
            duel.deck_x['trans'] = recognized_x.trans
            duel.deck_y['trans'] = recognized_y.trans
            # get duelists and decks for calculating elo
            duelist_x = get_user(duel.duelist_x)
            duelist_y = get_user(duel.duelist_y)
            duel['dr_x'], duel['dr_y'] = elo_add(
                duelist_x, duelist_y, duel.win)
            deck_x = db.Deck.find_one({"slug": recognized_x.slug})
            if recognized_x.slug == recognized_y.slug:
                deck_y = deck_x
            else:
                deck_y = db.Deck.find_one({"slug": recognized_y.slug})
                elo_add(deck_x, deck_y, duel.win)
            # update statistic
            deck_x.total += 1
            deck_y.total += 1
            duelist_x.total += 1
            duelist_y.total += 1
            if duel.win == Duel.WIN:
                duelist_x.wins += 1
                duelist_y.losses += 1
                deck_x.wins += 1
                deck_y.losses += 1
            elif duel.win == Duel.LOSE:
                duelist_x.losses += 1
                duelist_y.wins += 1
                deck_x.losses += 1
                deck_y.wins += 1
            duelist_x.save()
            duelist_y.save()
            deck_x.save()
            deck_y.save()
            duel.save()
            for collection in ('decks', 'users'):
                db.eval(Code(update_ranking % {'c': collection}))
            json = simplejson.dumps({'dr_x': round(duel['dr_x'], OUTPUT_ROUND),
                                     'dr_y': round(duel['dr_y'], OUTPUT_ROUND),
                                     'duel_id': str(duel._id)})
        except ValidationError:
            abort(400)
    return json


@app.route('/duels/<duel_id>', methods=['GET'])
@crossdomain(origin='*')
@json_response
def single(duel_id):
    try:
        duel = db.Duel.find_one({"_id": ObjectId(duel_id)})
    except:
        abort(400)
    if not duel:
        abort(404)
    return duel.to_json()


@app.route('/users/<username>')
@crossdomain(origin='*')
@json_response
def user(username):
    user = get_user(username)
    return user_to_json(user)


@app.route('/users/<username>/duels')
@crossdomain(origin='*')
@json_response
def user_duels(username):
    try:
        limit = int(request.args.get('limit', QUERY_LIMIT))
    except ValueError:
        abort(400)
    duels = db.Duel.find({"$or": [{'duelist_x': username},
                         {'duelist_y': username}]}).limit(limit)
    json = '{"duels": [%s]}' % ",".join(map(lambda x: x.to_json(), duels))
    return json


@app.route('/ranking/users')
@crossdomain(origin='*')
@json_response
def ranking_users():
    try:
        limit = int(request.args.get('limit', QUERY_LIMIT))
    except ValueError:
        abort(400)
    users = db.User.find().sort('rating', -1).limit(limit)
    return '{"users": [%s]}' % ','.join(map(user_to_json, users))


@app.route('/ranking/decks')
@crossdomain(origin='*')
@json_response
def ranking_duels():
    try:
        limit = int(request.args.get('limit', QUERY_LIMIT))
    except ValueError:
        abort(400)
    decks = db.Deck.find().sort('rating', -1).limit(limit)
    return '{"decks": [%s]}' % ','.join(map(deck_to_json, decks))
