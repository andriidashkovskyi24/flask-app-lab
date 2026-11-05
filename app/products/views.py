import os
import uuid
from flask import render_template, redirect, url_for, request, flash, current_app, abort
from werkzeug.utils import secure_filename
from app.products import product_bp
from app.forms import ProductForm
from app.models import ProductModel

product_model = ProductModel()

@product_bp.route('/')
def products_list():
    products = product_model.get_all()
    return render_template("products/products.html", products=products)

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = product_model.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template("products/detail_product.html", product=product)

@product_bp.route('/add', methods=['GET', 'POST'])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        image_filename = 'default.png'
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            f = form.image.data
            filename = secure_filename(f.filename)
            image_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads', image_filename)
            f.save(upload_path)
            
        product_model.create(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image=image_filename
        )
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.products_list'))
        
    return render_template('products/add.html', form=form)

@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def product_edit(product_id):
    product = product_model.get_by_id(product_id)
    if not product:
        abort(404)
        
    form = ProductForm(data=product)
    
    if form.validate_on_submit():
        image_filename = product.get('image', 'default.png')
        
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            f = form.image.data
            filename = secure_filename(f.filename)
            image_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads', image_filename)
            f.save(upload_path)
            
            if product.get('image') and product['image'] != 'default.png':
                old_img_path = os.path.join(current_app.root_path, 'static', 'uploads', product['image'])
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)
                    
        product_model.update(
            product_id=product_id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image=image_filename
        )
        flash('Товар успішно оновлено!', 'success')
        return redirect(url_for('products.products_list'))
        
    return render_template('products/edit.html', form=form, product=product)

@product_bp.route('/delete/<int:product_id>', methods=['POST'])
def product_delete(product_id):
    product = product_model.get_by_id(product_id)
    if not product:
        abort(404)
        
    if product.get('image') and product['image'] != 'default.png':
        img_path = os.path.join(current_app.root_path, 'static', 'uploads', product['image'])
        if os.path.exists(img_path):
            os.remove(img_path)
            
    product_model.delete(product_id)
    flash('Товар успішно видалено!', 'info')
    return redirect(url_for('products.products_list'))