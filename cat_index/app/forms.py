from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class UrlForm(Form):
    url = StringField('url', validators=[DataRequired()])
