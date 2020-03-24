from flask_wtf import Form
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Email, URL, Optional

class CardDataForm(Form):
    url = StringField(id="url", validators=[DataRequired(), URL()])
    logoFile = FileField(id="logoFile", validators=[DataRequired()])
    personName = StringField(id="personName", validators=[Optional()])
    companyName = StringField(id="companyName", validators=[Optional()])
    phone = StringField(id="phone", validators=[Optional()])
    email = StringField(id="email", validators=[Email(), Optional()])
    
