Gryphon
========

Tired of running thousands of gunicorn instances? tired of restarting the server to see the changes? Just drop your files just like you would do it with php and apache but instead with python and flask.

Usage
========
Download the source and upload your files to www/ directory. And you're done.

In every python file there has to be a method called ```run```. You can use everything flask provides from any python file since it will be called by the flask app.

For example:
```python
from flask import request

def run():
  return request.method
```

Run it
=========
To run it you just have to run the server.py file:
```bash
python server.py <gunicorn|tornado> <gunicorn params|tornado port>
```
