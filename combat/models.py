# -*- coding: utf-8 -*-
from datetime import datetime
from mongokit.schema_document import CustomType
from flask.ext.mongokit import Document

from combat.conf import DATETIME_FORMAT, START_RATING, PROVISIONAL_DUELS


main_deck_validator = lambda x: len(x) >= 40 and len(x) <= 60
extra_deck_validator = lambda x: len(x) >= 0 and len(x) <= 15
side_deck_validator = extra_deck_validator


class CustomDatetime(CustomType):
    mongo_type = unicode
    python_type = datetime
    init_type = None

    def to_bson(self, value):
        """convert type to a mongodb type"""
        return unicode(datetime.strftime(value, DATETIME_FORMAT))

    def to_python(self, value):
        """convert type to a python object"""
        if value is not None:
            return datetime.strptime(value, DATETIME_FORMAT)


class Duel(Document):

    WIN = 2
    DRAW = 1
    LOSE = 0

    __collection__ = 'duels'
    structure = {
        'duelist_x': unicode,
        'duelist_y': unicode,
        'deck_x': {
            'slug': unicode,
            'trans': unicode,
            'main': [int, ],
            'extra': [int, ],
            'side': [int, ],
        },
        'deck_y': {
            'slug': unicode,
            'trans': unicode,
            'main': [int, ],
            'extra': [int, ],
            'side': [int, ],
        },
        'win': int,
        'reason': int,
        'dr_x': float,
        'dr_y': float,
        'replay': unicode,
        'time': CustomDatetime(),
    }
    required = ['duelist_x', 'duelist_y', 'winner', 'reason',
                'deck_x.main', 'deck_y.main', 'replay', 'time']
    validators = {
        'deck_x.main': main_deck_validator,
        'deck_x.extra': extra_deck_validator,
        'deck_x.side': side_deck_validator,
        'deck_y.main': main_deck_validator,
        'deck_y.extra': extra_deck_validator,
        'deck_y.side': side_deck_validator,
    }
    use_dot_notation = True


class Deck(Document):
    __collection__ = 'decks'
    structure = {
        'slug': unicode,
        'trans': unicode,
        'rating': float,
        'ranking': int,
        'wins': int,
        'losses': int,
        'total': int,
    }

    @property
    def established(self):
        return self.total > PROVISIONAL_DUELS

    required = ['slug', 'trans', 'total', 'wins', 'losses', 'rating']
    default_values = {'total': 0, 'wins': 0, 'losses': 0,
                      'rating': START_RATING, 'ranking': 0}
    use_dot_notation = True


class User(Document):
    __collection__ = 'users'
    structure = {
        'username': unicode,
        'rating': float,
        'wins': int,
        'losses': int,
        'total': int,
        'ranking': int,
    }

    @property
    def established(self):
        return self.total > PROVISIONAL_DUELS

    required = ['username', 'rating', 'wins', 'losses', 'total']
    default_values = {'rating': START_RATING, 'wins': 0, 'losses': 0,
                      'total': 0, 'ranking': 0}
    use_dot_notation = True
