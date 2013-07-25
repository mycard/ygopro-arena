import os
HERE = os.path.dirname(__file__)

# Switch debugging
DEBUG = True
TESTING = True

# MongoDB Connection
MONGODB_DATABASE = 'combat'
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 9876
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

# Deck recognition
RULES_YAML = os.path.join(HERE, 'misc', 'rules.yml')
CARD_DATABASE = 'sqlite:///' + os.path.join(HERE, 'misc', 'cards.sqlite')

# Ranking
FUDICIAL_CREDIT = 10
FUDICIAL_CREDIT_FACTOR = 0.6
FUDICIAL_WIN_CREDIT = float(FUDICIAL_CREDIT)
FUDICIAL_LOSE_CREDIT = FUDICIAL_WIN_CREDIT * FUDICIAL_CREDIT_FACTOR
COUNT_CORRECTION_FACTOR = 0.3
RATE_CORRECTION_FACTOR = 0.4

# Misc
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
