Spine   = require('spine')

Spine.Model.host = "http://combat-api.torriacg.org"

class Duel extends Spine.Model
    @configure "Duel", "dueler_x", "dueler_y", "winner", "reason",
        "credit_x", "credit_y", "replay"

    @extend Spine.Model.Ajax

module.exports = Duel