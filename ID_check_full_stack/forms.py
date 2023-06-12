from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ID_Form(FlaskForm):
    id=StringField("ID")
    submit=SubmitField("Validate ID")