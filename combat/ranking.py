# -*- coding: utf-8 -*-
from flask import current_app
from combat.conf import (
    K,
    PROVISIONAL_DR,
    PROVISIONAL_DUELS
)
from combat.models import Duel


def elo_established(x, y, win):
    e = lambda d: float(1) / (1 + 10 ** (d / 400))

    def dr(e, win):
        s = (0, 0.5, 1)
        return K * (s[win] - e)
        
    ex = e(y.rating - x.rating)
    ey = e(x.rating - y.rating)
    return (dr(ex, win), dr(ey, 2 - win))


def elo_provisional(oneself, opponent, win):
    drs = (-PROVISIONAL_DR, 0, PROVISIONAL_DR)
    if not opponent.established:
        drs = map(lambda x: x / 2, drs)
    return (oneself.rating * oneself.total + opponent.rating +
            drs[win]) / (oneself.total + 1) - oneself.rating


def elo_add(x, y, win):
    edrs = elo_established(x, y, win)
    drs = []
    entities = (x, y)
    for i in xrange(0, 2):
        entity = entities[i]
        if entity.established:
            dr = edrs[i]
        else:
            dr = elo_provisional(entity, entities[(i + 1) % 2],
                                 abs(i * 2 - win))
        entity.rating += dr
        entity.save()
        drs.append(dr)
    current_app.logger.debug(drs)
    return drs


def rank(x):
    ranks = (
        ('Diamond', 2400),
        ('Platinum', 2200),
        ('Gold', 2000),
        ('Ruby', 1800),
        ('Pearl', 1600),
        ('Silver', 1400),
        ('Bronze', 1200),
        ('Iron', 1000),
        ('Stone', 800),
        ('Mud', 600),
        ('Dust', 400),
        ('Air', 200),
        ('Void', 0),
    )
    for rank_name, rank_lower_bound in ranks:
        if x.rating > rank_lower_bound:
            return rank_name
