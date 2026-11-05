import logging
from flask import request, redirect, url_for, render_template, abort, flash
from app import app
from app.forms import ContactForm  # Імпортуємо наш клас форми з forms.py
from app.models import ProductModel 


# Налаштування логування у файл app.log
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("index.html", agent=agent)

# Додаємо маршрут для резюме
@app.route('/resume')
def resume():
    return render_template("resume.html")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()  # 1. Створюємо об'єкт форми
    
    if form.validate_on_submit():
        # Збираємо дані
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        
        # 2. Записуємо дані у лог-файл
        logging.info(f"Контактна форма: Name={name}, Email={email}, Phone={phone}, Subject={subject}, Message={message}")
        
        flash('Повідомлення успішно відправлено та збережено в логах!', 'success')
        
        # 3. PRG патерн (Post/Redirect/Get)
        return redirect(url_for('contacts'))
        
    return render_template("contacts.html", form=form)