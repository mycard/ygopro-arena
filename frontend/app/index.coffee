require('lib/setup')

Spine = require('spine')
Main = require('controllers/main')
Header = require('controllers/header')
Duel = require('models/duel')
$ = Spine.$

class App extends Spine.Controller

    constructor: ->
        super
        @header = new Header
        @main = new Main
        @footer = new Footer
        @append @header, @main, @footer


        updateNav = (path) ->
            $(".nav li").removeClass()
            $(".nav li").has($('a[href="#' + path + '"]')).addClass('active')
            

        Spine.Route.setup()
        Spine.Route.bind("navigate", updateNav)
    

class Footer extends Spine.Controller

    className: 'footer'

    constructor: ->
        super
        @html require('views/footer')()


module.exports = App
    