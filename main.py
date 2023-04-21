from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor, CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from smtplib import SMTP
import os

my_email = os.environ.get("SMTP_EMAIL")
my_pw = os.environ.get("SMTP_PW")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SKEY")
Bootstrap5(app)
CKEditor(app)


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = CKEditorField('Message', validators=[DataRequired()])
    submit = SubmitField('Enquire')


@app.route('/')
def home():
    links = ["My Story", "Portfolio", "Contact"]
    return render_template("index.html", links=links)


@app.route('/about')
def about():
    links = ["Home", "Portfolio", "Contact"]
    return render_template("about.html", links=links)


@app.route('/portfolio')
def portfolio():
    links = ["Home", "My Story", "Contact"]
    return render_template("portfolio.html", links=links)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    links = ["Home", "My Story", "Portfolio"]
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        try:
            with SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_pw)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=my_email,
                    msg=f"Subject: Personal Page Enquiry from {name}\n\nName: {name}\nemail: {email}\n\n{message}",
                )
        except:
            flash("Sorry, the message did not go through.\nPlease send a direct enquiry to: steven.kim631@gmail.com.")
        else:
            flash("Successfully submitted!\nI'll get back to you as soon as possible.")
    return render_template("contact.html", links=links, form=form)


if __name__ == "__main__":
    app.run(debug=True)
