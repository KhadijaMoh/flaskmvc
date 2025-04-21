from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user, current_user, login_required
from .forms import RegistrationForm, LoginForm
from ..controllers.auth_controller import register_user, login_user_controller

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        success, user = register_user(form.username.data, form.password.data)
        if success:
            flash('Your account has been created! You are now able to log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(user, 'danger')
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('apartments.index'))
    form = LoginForm()
    if form.validate_on_submit():
        success, user = login_user_controller(form.username.data, form.password.data, form.remember.data)
        if success:
            flash('Logged in successfully!', 'success')
            return redirect(url_for('apartments.index'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('apartments.index'))