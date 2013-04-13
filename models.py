from flask.ext.mongokit import Document


main_deck_validator = lambda x:len(x) >= 40 and len(x) <= 60
extra_deck_validator = lambda x:len(x) >= 0 and len(x) <= 15


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
    }
    required_fields = ['dueler_x', 'dueler_y', 'winner', 'reason',
                       'deck_x.main', 'deck_y.main', 'credit_x',
                       'credit_y', 'replay']
    validators = {
        'deck_x.main': main_deck_validator,
        'deck_x.extra': extra_deck_validator,
        'deck_y.main': main_deck_validator,
        'deck_y.extra': extra_deck_validator,
    }
    use_dot_notation = True
