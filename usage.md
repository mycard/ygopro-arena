API Usage
=============

**Mycard Combat** provides a integrated solution to recording duels, deck
recognition and ranking, also expose a few RESTful APIs.

All of these APIs return `application/json`, some accept `application/json`
via `json` field in addition.

Duels
--------

### `/duels`

**Accept methods:** GET, POST

**Arguments:**

* limit: *int*, query limit for GET.
* json: *str*, json payload for POST.

GET method returns list of duels according to request condition. POST method
accept duel records.

**Example:**

GET `/duels?limit=1` will return json with root `duels`:

```
{
  "duels": [
    {
      "win": 2,
      "duelist_x": "abc",
      "duelist_y": "xyz",
      "dr_y": 0.0,
      "reason": 1,
      "dr_x": 200.0,
      "replay": "xxx.replay",
      "time": 1373127218000,
      "_id": {
        "$oid": "5221a5b3e4285f201c781c12"
      },
      "deck_x": {
        "main": [...omitted here 40 card ids...],
        "side": [],
        "extra": []
      },
      "deck_y": {
        "main": [...omitted here 40 card ids...],
        "side": [],
        "extra": []
      }
    }
  ]
}
```

POST `/duels` with payload `json`:

```
"{"duelist_x":"abc","duelist_y":"xyz","deck_x":{"main":[...omitted here 40 card ids...],"extra":[],"side":[]},"deck_y":{"main":[...omitted here 40 card ids...],"extra":[],"side":[]},"win":2,"reason":1,"replay":"xxx.replay","time":"2013-7-6 19:15:51"}"
```

can return:

```
{"duel_id":"5221cfb9e4285f25481d41f9","dr_y":-1.7,"dr_x":1.7}
```

in which `dr_x` and `dr_x` respectively indicate delta rating value of duelist
x and duelist y in this duel.


### `/duels/<duel_id>`

**Accept methods:** GET

Return single duel with specific id.

**Example:**

GET `/duels/5221a5b3e4285f201c781c12` may return:

```
{
  "win": 2,
  "duelist_x": "abc",
  "duelist_y": "xyz",
  "dr_y": 0.0,
  "reason": 1,
  "dr_x": 200.0,
  "replay": "xxx.replay",
  "time": 1373127218000,
  "_id": {
    "$oid": "5221a5b3e4285f201c781c12"
  },
  "deck_x": {
    "main": [...omitted here 40 card ids...],
    "side": [],
    "extra": []
  },
  "deck_y": {
    "main": [...omitted here 40 card ids...],
    "side": [],
    "extra": []
  }
}
```

Users
--------------

### `/users/<username>`

**Accept methods:** GET

Return single user with specific username.

**Example:**

GET `/users/abc` may return:

```
{
  "username": "abc",
  "ranking": 1,
  "rating": 1572.2,
  "wins": 46,
  "losses": 0,
  "rank": "Silver",
  "total": 46
}
```

### `/users/<username>/duels`

**Accept methods:** GET

Return duels that user with specific username involved in.

**Example:**

GET `/users/abc/duels` may return json with root `duels`:

```
{
  "duels": [
    {
      "win": 2,
      "duelist_x": "abc",
      "duelist_y": "xyz",
      "dr_y": 0.0,
      "reason": 1,
      "dr_x": 200.0,
      "replay": "xxx.replay",
      "time": 1373127218000,
      "_id": {
        "$oid": "5221a5b3e4285f201c781c12"
      },
      "deck_x": {
        "main": [...omitted here 40 card ids...],
        "side": [],
        "extra": []
      },
      "deck_y": {
        "main": [...omitted here 40 card ids...],
        "side": [],
        "extra": []
      }
    }
  ]
}
```

Ranking
----------

### `/ranking/users`

**Accept methods:** GET

**Arguments:**

* limit: *int*, query limit for GET.

Return top users.

**Example:**

GET `/ranking/users?limit=2` may return json with root `users`:

```
{
  "users": [
    {
      "username": "abc",
      "ranking": 1,
      "rating": 1572.2,
      "wins": 46,
      "losses": 0,
      "rank": "Silver",
      "total": 46
    },
    {
      "username": "xyz",
      "ranking": 2,
      "rating": 1027.8,
      "wins": 0,
      "losses": 46,
      "rank": "Iron",
      "total": 46
    }
  ]
}
```

### `/ranking/decks`

**Accept methods:** GET

**Arguments:**

* limit: *int*, query limit for GET.

Return top decks.

**Example:**

GET `/ranking/decks?limit=2` may return json with root `decks`:

```
{
  "decks": [
    {
      "ranking": 1,
      "trans": "荒行六武",
      "total": 46,
      "rating": 1572.2,
      "wins": 46,
      "losses": 0,
      "slug": "asceticism-sixsamurai",
      "rank": "Silver"
    },
    {
      "ranking": 2,
      "trans": "异虫",
      "total": 0,
      "rating": 1200.0,
      "wins": 0,
      "losses": 0,
      "slug": "worm",
      "rank": "Iron"
    }
  ]
}
```