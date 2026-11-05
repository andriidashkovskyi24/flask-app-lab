import os
from tinydb import TinyDB, Query

class ProductModel:
    def __init__(self):
        # Перевіряємо/створюємо папку data в корені проєкту
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Шлях до файлу products.json
        db_path = os.path.join(data_dir, 'products.json')
        self.db = TinyDB(db_path)
        self.table = self.db.table('products')
        
        # Якщо база порожня, автоматично додаємо початкові товари
        if len(self.table) == 0:
            self.init_default_products()

    def init_default_products(self):
        """Додає початкові товари, якщо база порожня"""
        default_items = [
            {
                'name': 'Ноутбук Lenovo',
                'description': 'Потужний ноутбук для роботи та програмування: Intel Core i5, 16 ГБ RAM, SSD 512 ГБ.',
                'price': 25000.00,
                'image': 'default.png'
            },
            {
                'name': 'Смартфон Samsung',
                'description': 'Сучасний смартфон із якісним екраном, ємною батареєю та чудовою камерою.',
                'price': 18500.00,
                'image': 'default.png'
            },
            {
                'name': 'Ігровий ПК',
                'description': 'Настільний комп’ютер для важких задач і геймінгу: дискретна відеокарта, швидкий процесор.',
                'price': 42000.00,
                'image': 'default.png'
            }
        ]
        self.table.insert_multiple(default_items)

    def get_all(self):
        """Отримати всі товари з бази"""
        return [ {**item, 'id': item.doc_id} for item in self.table.all() ]

    def get_by_id(self, product_id):
        """Отримати товар за ID"""
        item = self.table.get(doc_id=product_id)
        if item:
            return {**item, 'id': item.doc_id}
        return None

    def create(self, name, description, price, image):
        """Створити новий товар"""
        return self.table.insert({
            'name': name,
            'description': description,
            'price': float(price),
            'image': image
        })

    def delete(self, product_id):
        """Видалити товар за ID"""
        return self.table.remove(doc_ids=[product_id])

    def update(self, product_id, name, description, price, image=None):
        """Оновити інформацію про товар"""
        update_data = {
            'name': name,
            'description': description,
            'price': float(price)
        }
        # Якщо передано нове зображення, оновлюємо і його
        if image:
            update_data['image'] = image
            
        return self.table.update(update_data, doc_ids=[product_id])