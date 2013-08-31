from flask.ext.script import Manager

from combat.app import app, db
from combat.deck import DeckReco, FakeDeckRule

manager = Manager(app)


@manager.command
def updatedecks():
    """update decks according cards.sqlite"""
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
    print '%d decks added, %d decks deleted, total %d decks.' % (
        len(decks_to_add), len(decks_to_del), deck_amount)


if __name__ == "__main__":
    manager.run()
