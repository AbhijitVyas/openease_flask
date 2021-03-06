#!/usr/bin/env python

# This file starts the WSGI web application.
# - Heroku starts gunicorn, which loads Procfile, which starts runserver.py
# - Developers can run it from the command line: python runserver.py


from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from webrob.app_and_db import app, db
from webrob.pages.meshes import update_meshes
from webrob.startup.init_app import init_app


def _config_is_debug():
    # if environment variable 'EASE_DEBUG' is set to true, then
    # 'DEBUG' in app.config will be set to true by init_app.py
    return 'DEBUG' in app.config and app.config['DEBUG']


def _run_debug_server():
    # print 'Run web server in DEBUG mode'
    # app.run(host='0.0.0.0', debug=True)
    print 'DEBUG mode currently does not work'
    print 'Start normal web server'
    _run_server()


def _run_server():
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    print 'Web server is running. Listening on {}'.format(5000)
    IOLoop.instance().start()


init_app(app, db)

# Start a development web server if executed from the command line
if __name__ == '__main__':
    update_meshes()
    if _config_is_debug():
        _run_debug_server()
    else:
        _run_server()
