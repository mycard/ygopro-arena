# -*- coding: utf-8 -*-
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from combat.conf import RULES_YAML, CARD_DATABASE

Base = declarative_base()
engine = create_engine(CARD_DATABASE, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


_CARD_TYPES = ('monster', 'spell', 'trap', 'normal', 'effect', 'fusion',
               'ritual', 'trapmonster', 'spirit', 'union', 'gemini', 'tuner', 'synchro',
               'token', 'quickplay', 'continuous', 'equip', 'field', 'counter', 'flip',
               'toon', 'xyz')

_ATTRIBUTES = ('earth', 'water', 'fire', 'wind', 'light', 'dark', 'divine')

_RACES = ('warrior', 'spellcaster', 'fairy', 'fiend', 'zombie', 'machine',
          'aqua', 'pyro', 'rock', 'winged_beast', 'plant', 'insect', 'thunder',
          'dragon', 'beast', 'beast_warrior', 'dinosaur', 'fish', 'sea_serpent',
          'reptile', 'psychic', 'divine_beast', 'creator_god')

_FLAGS = {
    'card_type': _CARD_TYPES,
    'attribute': _ATTRIBUTES,
    'race': _RACES,
}


def get_flag(type_, str_):
    strs = str_.split(' ')
    flag = lambda s: 2 ** _FLAGS[type_].index(s)
    return reduce(lambda x, y: x + y, map(flag, strs))


class Card(Base):

    __tablename__ = 'datas'

    id = Column(Integer, primary_key=True)
    setcode = Column(Integer)
    type = Column(Integer)
    level = Column(Integer)
    race = Column(Integer)
    attribute = Column(Integer)


class CardText(Base):

    __tablename__ = 'texts'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class DeckRule(object):

    parent = None

    def __init__(self, slug, rule):
        meta = rule[0]
        self.slug = slug
        self.predications = rule[1:]
        self.trans = meta['trans']
        if meta.has_key('parent'):
            self.parent = meta['parent']


class FakeDeckRule(DeckRule):

    def __init__(self, slug='none', rule=[]):
        self.slug = 'unknown'
        self.predications = []
        self.trans = u'未知卡组'


class DeckReco(object):

    """Deck recognition"""

    def __init__(self):
        with open(RULES_YAML, 'r') as f:
            document = f.read()
            self._rules = yaml.load(document)
        self.rules = list()
        for k, v in self._rules.iteritems():
            self.rules.append(DeckRule(k, v))
        self.roots = list()
        self.subs = dict()
        for rule in self.rules:
            if rule.parent is None:
                self.roots.append(rule)
            else:
                if self.subs.has_key(rule.parent):
                    self.subs[rule.parent].append(rule)
                else:
                    self.subs[rule.parent] = [rule, ]

    def validate(self, type_, count, *args, **kwargs):
        method = getattr(self, type_)
        return len([card for card in self.deck
                    if method(card, *args, **kwargs)]) >= count

    def set(self, card, set_flag):
        return not card.setcode ^ set_flag

    def name(self, card, name):
        return name in card.name

    def card_type(self, card, card_type):
        return card.type is get_flag('card_type', card_type)

    def attribute(self, card, attr):
        return card.attr & get_flag('attribute', attr)

    def race(self, card, race):
        return card.race & get_flag('race', race)

    def level(self, card, level):
        operator = level[-1]
        level = int(level[:-1])
        if operator is '+':
            return card.level >= level
        elif operator is '-':
            return card.level <= level

    def apply_rule(self, rule):
        is_recognized = True
        for predication in rule.predications:
            keys = predication.keys()
            keys.remove('count')
            rule_type = keys[0]
            is_recognized &= self.validate(rule_type, predication['count'],
                                           predication[rule_type])
        return is_recognized

    def summarize(self):
        for root in self.roots:
            is_in_root = self.apply_rule(root)
            if is_in_root:
                if self.subs.has_key(root.slug):
                    for sub in self.subs[root.slug]:
                        if self.apply_rule(sub):
                            return sub
                return root
        return FakeDeckRule()

    def parse_ydk(self, ydk):
        self.deck = list()
        f = open(ydk, 'r')
        for line in f:
            if '#' in line or '!' in line:
                continue
            card_id = int(line)
            card = session.query(Card).filter(Card.id == card_id).one()
            card.name = unicode(session.query(CardText).filter(
                CardText.id == card_id).one().name)
            self.deck.append(card)
        return self.summarize()

    def parse_ids(self, ids):
        self.deck = list()
        for card_id in ids:
            card = session.query(Card).filter(Card.id == card_id).one()
            card.name = unicode(session.query(CardText).filter(
                CardText.id == card_id).one().name)
            self.deck.append(card)
        return self.summarize()
