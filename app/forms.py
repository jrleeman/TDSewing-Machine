from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ServerPropertiesForm(FlaskForm):
    """
    Form to specify the host institution of the server.
    """
    institution_name = StringField('Institution Name', validators=[DataRequired()])
    institution_website = StringField('Institution Website', validators=[DataRequired()])
    logo_url = StringField('Logo URL', validators=[DataRequired()])
    logo_alttext = StringField('Logo Alternate Text', validators=[DataRequired()])
    submit = SubmitField('Create Configuration')
