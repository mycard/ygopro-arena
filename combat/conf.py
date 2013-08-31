# -*- coding: utf-8 -*-
import os
HERE = os.path.dirname(__file__)

# Switch debugging
DEBUG = True
TESTING = True

# MongoDB Connection
MONGODB_DATABASE = 'combat'
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

# Deck recognition
RULES_YAML = os.path.join(HERE, 'misc', 'rules.yml')
CARD_DATABASE = 'sqlite:///' + os.path.join(HERE, 'misc', 'cards.sqlite')

# ELO Ranking
K = 40
START_RATING = float(1200)
PROVISIONAL_DUELS = 10
PROVISIONAL_DR = 400
OUTPUT_ROUND = 1

# Misc
QUERY_LIMIT = 20
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
