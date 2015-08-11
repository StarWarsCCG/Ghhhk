from flask.ext.wtf import Form

from wtforms import TextField, TextAreaField, SubmitField, validators


class ContactForm(Form):
    name = TextField("Name", [validators.Required()])
    email = TextField("Email", [validators.Required(), validators.email()])
    subject = TextField("Subject", [validators.Required()])
    message = TextAreaField("Message", [validators.Required()])
    submit = SubmitField("Send")