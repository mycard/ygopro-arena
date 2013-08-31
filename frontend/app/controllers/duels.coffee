Spine = require('spine')
Duel = require('models/duel')
$ = Spine.$


class Duels extends Spine.Controller

    className: 'show-duels'

    events:
        'submit #duel-query' : 'query'

    constructor: ->
        super
        Duel.bind 'refresh change', @render
        Duel.fetch({data: "limit=10"})

    render: =>
        duels = Duel.all()
        @html require('views/duels')(duels: duels, username: @username)
        $('#duel-query').children('input').focus()

    query: (e) ->
        e.preventDefault()
        @username = $(e.target).children('input').val()
        if @username
            Duel.fetch({data: 'duelist=' + @username})
        Duel.refresh([], {clear: true})
        @navigate('/duels')

module.exports = Duels
