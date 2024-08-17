from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import RegistrationForm, LoginForm
from . import db
from .models import Idea

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Create a new user instance
        new_user = User(username=username, email=email)
        new_user.set_password(password)  
        db.session.add(new_user)
        db.session.commit()

        # Log in the user after registration
        login_user(new_user)

        return redirect(url_for('main.home'))

    return render_template('register.html', form=form) 


@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user_ideas = Idea.query.filter_by(user_id=current_user.id).all()  

    return render_template('dashboard.html', ideas=user_ideas)


@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
