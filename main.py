from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'learnpython407'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'learnpython407@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('APP_PW')

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date = request.form['avail_date']
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        occupation = request.form['occupation']

        form = Form(fname=first_name, lname=last_name, email=email, 
                    date=date_obj, occupation=occupation)
        
        db.session.add(form)
        db.session.commit()

        message_body = f'Thank you for your submission, {first_name}.' \
                        f'Here are your data:\n{first_name}\n{last_name}\n{date}\n{occupation}\n'\
                        f'Thank you'
        message = Message(subject='New form submitted',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash(f"{first_name}'s, form was submitted successfully!", 'success')

    return render_template("index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)