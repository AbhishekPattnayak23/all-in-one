from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.auth import bp
from app.auth.forms import LoginForm
from app.models.user import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Update last login
            from datetime import datetime
            user.last_login = datetime.utcnow()
            from app.extensions import db
            db.session.commit()
            
            # Log in user
            login_user(user)
            
            # Handle redirect or default to dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
                
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.login'))
