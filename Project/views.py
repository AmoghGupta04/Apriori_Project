"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from Project import app

import pandas as pd
from io import BytesIO

from Project.ml import Mlalgo


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )



@app.route('/team')
def team():
    """Renders the contact page."""
    return render_template(
        'team.html',
        title='Team JIO',
        year=datetime.now().year,
        message='Team Info Page'
    )


@app.route('/ml')
def ml():
    """Renders the ml page."""
    return render_template(
        'ml.html',
        title='Machine Learning',
        year=datetime.now().year,
        message='ML Analysis Page'
    )




@app.route('/run', methods = ['POST', 'PUT'])
def run():
    """Renders the ihub page."""
    file = request.files['file']

    if file:
            file_contents = file.read()
            datalist = Mlalgo().run(file_contents)
            return render_template('output.html',table_data=datalist)

    else:
        return 'No file selected!'
