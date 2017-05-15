#from flask_wtf import Form
from wtforms import SubmitField, TextField, TextAreaField, validators, Form

class CreateDatasetForm(Form):
    name = TextField('name', validators=[validators.DataRequired()])
    path = TextField('path', validators=[validators.DataRequired()])
    metadata = TextAreaField('metadata', validators=[validators.DataRequired()])
    submit = SubmitField('submit')

class CreateFeatureCollectionForm(Form):
        name = TextField('name', validators=[validators.DataRequired()])
        path = TextField('path', validators=[validators.DataRequired()])
        xml = TextAreaField('xml', validators=[validators.DataRequired()])
        pqact = TextAreaField('pqact', validators=[validators.DataRequired()])
        submit = SubmitField('submit')
