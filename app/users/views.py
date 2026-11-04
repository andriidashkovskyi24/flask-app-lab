from flask import render_template, request, redirect, url_for, session, flash, make_response
from app.users import users_bp

# Заглушка для користувача
VALID_USER = {
    "username": "user1",
    "password": "12345"
}

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Перевірка даних автентифікації
        if username == VALID_USER['username'] and password == VALID_USER['password']:
            session['username'] = username
            flash('Успішний вхід!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Wrong data! Try again!', 'danger')
            return redirect(url_for('users.login'))
            
    return render_template('users/login.html')

@users_bp.route('/profile')
def profile():
    # Перевірка, чи користувач є в сесії
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'danger')
        return redirect(url_for('users.login'))
        
    username = session['username']
    cookies = request.cookies
    theme = request.cookies.get('theme', 'light')
    return render_template('users/profile.html', username=username, cookies=cookies, theme=theme)

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли із системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/profile/set_cookie', methods=['POST'])
def set_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))
        
    key = request.form.get('cookie_name')
    value = request.form.get('cookie_value')
    max_age = request.form.get('cookie_age', type=int)
    
    response = make_response(redirect(url_for('users.profile')))
    if key and value:
        response.set_cookie(key, value, max_age=max_age)
        flash(f'Кукі "{key}" успішно додано!', 'success')
    else:
        flash('Будь ласка, заповніть ключ та значення кукі!', 'danger')
    return response

@users_bp.route('/profile/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))
        
    key = request.form.get('cookie_name')
    response = make_response(redirect(url_for('users.profile')))
    if key:
        response.set_cookie(key, '', expires=0)
        flash(f'Кукі "{key}" успішно видалено!', 'info')
    return response

@users_bp.route('/profile/clear_cookies')
def clear_cookies():
    if 'username' not in session:
        return redirect(url_for('users.login'))
        
    response = make_response(redirect(url_for('users.profile')))
    for cookie_key in request.cookies:
        response.set_cookie(cookie_key, '', expires=0)
    flash('Всі кукі успішно видалено!', 'warning')
    return response

@users_bp.route('/profile/change_theme/<theme_name>')
def change_theme(theme_name):
    if 'username' not in session:
        return redirect(url_for('users.login'))
    
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('theme', theme_name, max_age=60*60*24*30)  # Зберігаємо на місяць
    flash(f'Колірну схему змінено на: {theme_name}', 'success')
    return response