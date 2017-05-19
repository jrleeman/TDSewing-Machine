"""Contains forms for TDSewing Machine."""


from wtforms import (Form, HiddenField, SelectField, SubmitField,
                     TextAreaField, TextField, validators)


class CreateDatasetForm(Form):
    """Form for dataset creation."""

    name = TextField('name', validators=[validators.DataRequired()])
    path = SelectField('path')
    xml = TextAreaField('xml')
    metadata = TextAreaField('metadata', validators=[validators.DataRequired()])
    id = HiddenField('_id')
    submit = SubmitField('submit')


class CreateFeatureCollectionForm(Form):
    """Form for feature collection creation."""

    name = TextField('name', validators=[validators.DataRequired()])
    dataset = SelectField('dataset', validators=[validators.DataRequired()])
    xml = TextAreaField('xml', validators=[validators.DataRequired()])
    pqact = TextAreaField('pqact', validators=[validators.DataRequired()])
    submit = SubmitField('submit')
