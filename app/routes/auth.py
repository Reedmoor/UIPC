from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.auth import LoginForm, RegisterForm, PasswordChangeForm, ProfileEditForm
from app.models.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            flash('Неверный email или пароль', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Данный email уже зарегистрирован', 'danger')
            return render_template('auth/register.html', form=form)
        
        user = User(
            name=form.name.data,
            email=form.email.data,
            role='user'  # Обычный пользователь по умолчанию
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешно завершена! Теперь вы можете войти', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    
    if form.validate_on_submit():
        # Проверка текущего пароля
        if not current_user.check_password(form.current_password.data):
            flash('Текущий пароль введен неверно', 'danger')
            return render_template('auth/change_password.html', form=form)
            
        # Установка нового пароля
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('Пароль успешно изменен', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('auth/change_password.html', form=form)

@auth_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm(obj=current_user)
    
    if form.validate_on_submit():
        # Проверить, не используется ли email другим пользователем
        if form.email.data != current_user.email:
            user_with_email = User.query.filter_by(email=form.email.data).first()
            if user_with_email:
                flash('Этот email уже используется другим пользователем', 'danger')
                return render_template('auth/edit_profile.html', form=form)
        
        # Обновление данных профиля
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash('Профиль успешно обновлен', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('auth/edit_profile.html', form=form) 