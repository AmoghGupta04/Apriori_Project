"""
This script runs the FlaskWebProject application using a development server.
"""

from os import environ
from Project import app
# print(f"this is runserver.py:{__name__}")
if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(host=HOST, port=PORT, debug=True)
