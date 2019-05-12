from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort,g
from flask_login import login_user, current_user, logout_user, login_required
from web import app, db, bcrypt, mail
from web.forms import RegistrationForm, LoginForm
from web.models import User, Messages, Phonecall, Emails




@app.route("/")
def index():
    return render_template('index.html')


@app.route("/blog")
def blog():
    return render_template('blog.html')



@app.route("/blog1")
def blog1():
    return render_template('blog1.html')



@app.route("/contact")
def contact():
    return render_template('contact.html')



@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/services")
def services():
    return render_template('services.html')








@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            db.session.commit()
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/new_message", methods=['GET', 'POST'])
def new_message():
    if request.method == "POST":
        message = Messages(names=request.form['name'],emails=request.form['email'],subjects=request.form['subject'],messages=request.form['message'])
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent!', 'success')
    return redirect(url_for('contact'))




@app.route("/new_call", methods=['GET', 'POST'])
def new_call():
    if request.method == "POST":
        message = Phonecall(names=request.form['author'],emails=request.form['email0'],phones=request.form['phone'])
        db.session.add(message)
        db.session.commit()
        flash('Your request was successful!', 'success')
    return redirect(url_for('index'))



@app.route("/emails", methods=['GET', 'POST'])
def emails():
    if request.method == "POST":
        message = Emails(emails=request.form['ss'])
        db.session.add(message)
        db.session.commit()
        flash('Your request was successful!', 'success')
    return redirect(url_for('index'))




@app.route("/get_message")
def get_message():
    allmessages = Messages.query.all()
    return render_template('get_message.html',allmessages=allmessages)



@app.route("/get_call")
def get_call():
    allcalls = Phonecall.query.all()
    return render_template('get_call.html',allcalls=allcalls)



@app.route("/get_email")
def get_email():
    allemails = Emails.query.all()
    return render_template('get_emails.html',allemails=allemails)
