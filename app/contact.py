import logging
from flask import Blueprint, render_template, redirect, url_for, flash
from forms import ContactForm

# Створюємо маленький окремий модуль для контактів
contact_bp = Blueprint('contact_bp', __import__('__main__').__name__)

# Налаштування логування (створить файл app.log)
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        
        # Записуємо у лог
        logging.info(f"Контактна форма: Name={name}, Email={email}, Phone={phone}, Subject={subject}, Message={message}")
        
        flash('Повідомлення успішно відправлено та збережено в логах!', 'success')
        return redirect(url_for('contact_bp.contact'))
        
    return render_template('contacts.html', form=form)