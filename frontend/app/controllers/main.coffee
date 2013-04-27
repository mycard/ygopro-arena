Spine = require('spine')
Duel = require('models/duel')
Duels = require('controllers/duels')
$ = Spine.$


class About extends Spine.Controller

    className: 'about'

    constructor: ->
        super
        @active @render

    render: ->
        @html require('views/about')()

class Main extends Spine.Stack

    controllers:
        duels: Duels
        about: About

    routes:
        '/duels': 'duels'
        '/about': 'about'

    default: 'about'

module.exports = Main