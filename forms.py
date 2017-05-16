#from flask_wtf import Form
from wtforms import SubmitField, TextField, TextAreaField, validators, Form, HiddenField, SelectField

class CreateDatasetForm(Form):
    name = TextField('name', validators=[validators.DataRequired()])
    path = SelectField('path', choices=[('t1', 'Test 1'), ('t2', 'Test 2')], validators=[validators.DataRequired()])
    xml = TextAreaField('xml', validators=[validators.DataRequired()])
    metadata = TextAreaField('metadata', validators=[validators.DataRequired()])
    submit = SubmitField('submit')

class CreateFeatureCollectionForm(Form):
    name = TextField('name', validators=[validators.DataRequired()])
    dataset = SelectField('dataset', choices=[('t1', 'Test 1'), ('t2', 'Test 2')], validators=[validators.DataRequired()])
    xml = TextAreaField('xml', validators=[validators.DataRequired()])
    pqact = TextAreaField('pqact', validators=[validators.DataRequired()])
    submit = SubmitField('submit')
