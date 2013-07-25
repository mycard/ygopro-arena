from datetime import datetime
from mongokit.schema_document import CustomType
from flask.ext.mongokit import Document

from combat.conf import DATETIME_FORMAT


main_deck_validator = lambda x: len(x) >= 40 and len(x) <= 60
extra_deck_validator = lambda x: len(x) >= 0 and len(x) <= 15


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
    __collection__ = 'duels'
    structure = {
        'dueler_x': unicode,
        'dueler_y': unicode,
        'deck_x': {
            'main': [int, ],
            'extra': [int, ],
        },
        'deck_y': {
            'main': [int, ],
            'extra': [int, ],
        },
        'winner': bool,
        'reason': int,
        'credit_x': int,
        'credit_y': int,
        'replay': unicode,
        'time': CustomDatetime(),
    }
    required = ['dueler_x', 'dueler_y', 'winner', 'reason',
                'deck_x.main', 'deck_y.main', 'replay', 'time']
    validators = {
        'deck_x.main': main_deck_validator,
        'deck_x.extra': extra_deck_validator,
        'deck_y.main': main_deck_validator,
        'deck_y.extra': extra_deck_validator,
    }
    use_dot_notation = True


class Deck(Document):
    __collection__ = 'decks'
    structure = {
        'slug': unicode,
        'trans': unicode,
        'win_count': int,
        'lose_count': int,
        'count': int,
    }
    required = ['slug', 'trans', 'count', 'win_count', 'lose_count']
    default_values = {'count': 0, 'win_count': 0, 'lose_count': 0}
    use_dot_notation = True
