#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
from gryphon import gryphon as app

show_help = False

if len(sys.argv) > 1:
    server = sys.argv[1]
    if len(sys.argv) > 2:
        params = sys.argv[2]
    else:
        params = ''
        
    if server == 'tornado':
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        http_server = HTTPServer(WSGIContainer(app))
        if not params:
            params = 5000
        else:
            try:
                params = int(params)
            except:
                params = 5000
        http_server.listen(params)
        IOLoop.instance().start()
    elif 'gunicorn':
        os.system("gunicorn %s gryphon:gryphon" % params)
    else:
        show_help = True
else:
    show_help = True
    
if show_help:
    print("Usage:")
    print("  python server.py <server> <params>")
    print("    - server: the desired server, gunicorn or tornado")
    print("    - params: the port number for tornado, gunicorn params for gunicorn")