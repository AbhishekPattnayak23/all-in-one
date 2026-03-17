from flask import render_template, redirect, url_for, flash, request
from app import db
from app.auth import auth
from app.auth.forms import RegistrationForm
from app.models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new user with password hashing
            user = User(
                username=form.username.data.strip().lower(),
                email=form.email.data.strip().lower()
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            # Security: Log registration attempt
            print(f"[SECURITY] New registration: {user.username} - {user.email}")
            
            flash('Registration successful! Please check your email for verification.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            print(f"[SECURITY] Registration error: {str(e)}")
    
    return render_template('auth/register.html', form=form)
    
@auth.route('/login')
def login():
    return render_template('auth/login.html')
