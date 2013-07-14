#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, send_from_directory, abort
from werkzeug.routing import BaseConverter
import os

gryphon = Flask(__name__)

modules = {}

class RegexRouteConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexRouteConverter, self).__init__(url_map)
        self.regex = items[0]
        
gryphon.url_map.converters['regex'] = RegexRouteConverter

ALLOWED_EXTS = [
    'html',
    'css',
    'js',
    'py',
    'png',
    'gif',
    'svg',
    'jpg',
    'jpeg',
    'bmp',
    'swf',
    'mp3',
    'mp4',
    'htm'
]

@gryphon.route('/<regex(".*"):route>')
def handler(route):
    if 'pyc' in os.path.abspath(__file__):
        abs_path = os.path.abspath(__file__).replace('gryphon.pyc', '')
    else:
        abs_path = os.path.abspath(__file__).replace('gryphon.pyc', '')
        
    if route:
        if '.' in route and route[route.rfind('.')+1:] in ALLOWED_EXTS:
            # It's a file
            if '.py' in route:
                # Python file
                file = "www."+route[:route.rfind('.py')].replace('/', '.')
                file_path = abs_path + "www/" + route[:route.rfind('.py')+3]
                run_mode = 1
            else:
                # Static file
                run_mode = 2
        else:
            # It's not a file but a module
            file = 'www.'+route.replace('/', '.')
            file_path = abs_path + "www/" + route + '.py'
            run_mode = 1
    else:
        file = 'www.index'
        file_path = abs_path + 'www/index.py'
        run_mode = 1

    if run_mode == 1:
        if os.path.exists(file_path):
            try:
                if file in modules.keys():
                    try:
                        modules[file] = reload(modules[file])
                    except:
                       modules[file] = __import__(file, fromlist=['*']) 
                else:
                    modules[file] = __import__(file, fromlist=['*'])
            except:
                return "Import error: error occurred importing the requested module."

            try:
                if 'run' in dir(modules[file]):
                    return modules[file].run()
                else:
                    return "Run error: requested module does not contain a run method."
            except:
                return "Run error: unexpected error occurred running the requested module."
        else:
            abort(404)
    else:
        file_path = abs_path + 'www'
        if '/' in route:
            file_path += '/' + route[:route.rfind('/')]
            file_name = route[route.rfind('/')+1:]
        else:
            file_name = route
            
        if not os.path.exists(file_path + '/' + file_name):
            abort(404)

        return send_from_directory(file_path, file_name)
    
if __name__ == "__main__":
    gryphon.run(debug=True, host='0.0.0.0', port=8888)