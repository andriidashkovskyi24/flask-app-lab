from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.py")

# Головні views
from app import views

# Реєстрація блюпринта users (виправляємо user_bp на users_bp)
from app.users.views import users_bp
app.register_blueprint(users_bp)

# Реєстрація блюпринта products
from app.products.views import product_bp
app.register_blueprint(product_bp)