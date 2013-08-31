Installation
===============

Install requirements
-------------------------

Example steps in Ubuntu 12.04:

```shell
$ sudo apt-get install uwsgi
$ git clone git@github.com:mycard/mycard-combat.git /somewhere/mycard_combat
$ cd /somewhere/mycard_combat
$ sudo pip install -r requirements.txt
```

Some manual works
---------------------

1. Put `cards.cdb` of ygopro in `/combat/misc` as `cards.sqlite` for deck
   recognization. 
2. Fill in mongodb connection fields in `conf.py`.
3. Enter `/somewhere/mycard_combat`.
4. Run `python manage.py updatedecks`.

Configure uwsgi
------------------

Write `/etc/uwsgi/apps-avaliable/combat.ini` as following:

```ini
[uwsgi]
plugins = python
chdir = /somewhere/mycard_combat
module = combat.app
callable = app
socket = /tmp/combat.sock
vaccum = true
```

Than make a soft link and restart uwsgi to enable it:

```
$ sudo ln -s /etc/uwsgi/apps-available/combat.ini /etc/uwsgi/apps-enabled/combat.ini
$ sudo service uwsgi restart
```

Configure nginx
------------------

Write `/etc/nginx/sites-avaliable/combat` as following:

```
server {
    listen 80;
    server_name example.com
    error_log /var/log/nginx/combat_error;

    location / {
        try_file $uri @app;
    }
    location @app {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/combat.sock
    }
}
```

Then make a soft link and reload nginx configuration to enable it:

```
$ sudo ln -s /etc/nginx/sites-available/combat /etc/nginx/sites-enabled/combat
$ sudo service nginx reload
```
