#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Gryphon server

Usage:
  server.py gunicorn
  server.py gunicorn <gunicorn_params>
  server.py tornado
  server.py tornado <tornado_port>
  server.py (-h | --help)

Options:
  -h --help     Show this screen.

"""

from __future__ import print_function
import sys
import os
from gryphon import gryphon as app
from docopt import docopt

arguments = docopt(__doc__, version='Gryphon server 1.0')

if arguments['gunicorn']:
    try:
        os.system("gunicorn %s gryphon:gryphon" % arguments['gunicorn_params'])
    except KeyError:
        os.system("gunicorn gryphon:gryphon")
elif arguments['tornado']:
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    try:
        port = int(arguments['tornado_port'])
    except:
        port = 5000
    http_server.listen(params)
    IOLoop.instance().start()
else:
    print(__doc__)