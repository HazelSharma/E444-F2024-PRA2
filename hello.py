from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment 
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string2'
bootstrap = Bootstrap(app)
moment = Moment(app)

def validate_uoft_email(form, field):
    email = field.data
    if '@' not in email:
        raise ValidationError('Please enter a valid email address, missing @.')
    if 'utoronto' not in email:
        raise ValidationError('Please enter a UofT email address, missing "utoronto".')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), validate_uoft_email])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    email = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email')) 

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
# <p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
# <p>That way {{ moment(current_time).fromNow(refresh=True) }}.</p>