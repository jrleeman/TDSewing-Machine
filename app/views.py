from flask import render_template

from app import app
from .forms import ServerPropertiesForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    form = ServerPropertiesForm()
    if form.validate_on_submit():
        flash('Configuration Sucessful! Check your email.')
    return render_template('configure.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')
