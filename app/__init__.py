from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.py")

# Головні views
from app import views

# Реєстрація блюпринта users
from app.users.views import user_bp
app.register_blueprint(user_bp)

# Реєстрація блюпринта products
from app.products.views import product_bp
app.register_blueprint(product_bp)