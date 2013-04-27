Spine = require('spine')
Duel = require('models/duel')
$ = Spine.$

class Header extends Spine.Controller

    elements:
        'li': 'items'

    className: 'header'

    events:
        'click li>a': 'click'

    constructor: ->
        super
        @html require('views/header')()

    click: (e) ->
        item = $(e.target).parent()
        @items.removeClass 'active'
        item.addClass 'active'

module.exports = Header
