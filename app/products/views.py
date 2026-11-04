from flask import render_template
from app.products import product_bp

# Масив товарів із завдання
products_list = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам'яті та SSD на 512 ГБ."
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год."
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "content": "Настільний комп'ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD."
    }
]

@product_bp.route('/')
def all_products():
    return render_template("products/products.html", products=products_list)

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    # Шукаємо товар за його id
    prod = next((p for p in products_list if p["id"] == product_id), None)
    return render_template("products/detail_product.html", product=prod)