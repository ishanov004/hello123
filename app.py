from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('DELETE_SECRET', os.urandom(24).hex())
DATABASE = os.getenv('DB_NAME', 'equipment.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            country TEXT,
            price REAL,
            delivery REAL,
            date TEXT,
            quantity INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id INTEGER,
            category_id INTEGER,
            date TEXT,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (equipment_id) REFERENCES equipment (id),
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buy')
def buy_index():
    conn = get_db_connection()
    items = conn.execute('''
        SELECT e.id, e.name, c.name as category, e.country, e.price, e.delivery, e.date, e.quantity
        FROM equipment e LEFT JOIN categories c ON e.category_id = c.id
    ''').fetchall()
    conn.close()
    return render_template('buy/index.html', items=items)

@app.route('/buy/add', methods=['GET', 'POST'])
def buy_add():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    countries = conn.execute('SELECT * FROM countries').fetchall()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category']
        country = request.form['country']
        price = float(request.form['price'])
        delivery = float(request.form['delivery'])
        date = request.form['date']
        quantity = int(request.form['quantity'])
        conn.execute('INSERT INTO equipment (name, category_id, country, price, delivery, date, quantity) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (name, category_id, country, price, delivery, date, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('buy_index'))
    return render_template('buy/add.html', categories=categories, countries=countries)

@app.route('/buy/edit/<int:item_id>', methods=['GET', 'POST'])
def buy_edit(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM equipment WHERE id = ?', (item_id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    countries = conn.execute('SELECT * FROM countries').fetchall()
    if request.method == 'POST':
        conn.execute('''
            UPDATE equipment SET name=?, category_id=?, country=?, price=?, delivery=?, date=?, quantity=?
            WHERE id=?
        ''', (
            request.form['name'],
            request.form['category'],
            request.form['country'],
            float(request.form['price']),
            float(request.form['delivery']),
            request.form['date'],
            int(request.form['quantity']),
            item_id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('buy_index'))
    return render_template('buy/edit.html', item=item, categories=categories, countries=countries)

@app.route('/buy/delete/<int:item_id>', methods=['GET', 'POST'])
def buy_delete(item_id):
    if request.method == 'POST':
        code = request.form.get('code')
        if code == os.getenv('DELETE_SECRET'):
            conn = get_db_connection()
            conn.execute('DELETE FROM equipment WHERE id = ?', (item_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('buy_index'))
        else:
            flash('Неверный код удаления')
            return redirect(url_for('buy_delete', item_id=item_id))
    return render_template('buy/confirm_delete.html', item_id=item_id)

@app.route('/sales')
def sales_index():
    conn = get_db_connection()
    sales = conn.execute('''
        SELECT s.id, e.name AS equipment, c.name AS category, s.date, s.quantity, s.price
        FROM sales s
        LEFT JOIN equipment e ON s.equipment_id = e.id
        LEFT JOIN categories c ON s.category_id = c.id
    ''').fetchall()
    conn.close()
    return render_template('sales/index.html', sales=sales)

@app.route('/sales/add', methods=['GET', 'POST'])
def sales_add():
    conn = get_db_connection()
    equipment = conn.execute('SELECT * FROM equipment WHERE quantity > 0').fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    if request.method == 'POST':
        equipment_id = int(request.form['equipment'])
        category_id = int(request.form['category'])
        date = request.form['date']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        item = conn.execute('SELECT quantity FROM equipment WHERE id = ?', (equipment_id,)).fetchone()
        if item and item['quantity'] >= quantity:
            conn.execute('INSERT INTO sales (equipment_id, category_id, date, quantity, price) VALUES (?, ?, ?, ?, ?)',
                         (equipment_id, category_id, date, quantity, price))
            conn.execute('UPDATE equipment SET quantity = quantity - ? WHERE id = ?', (quantity, equipment_id))
            conn.commit()
            conn.close()
            return redirect(url_for('sales_index'))
        else:
            flash(f'Ошибка: на складе только {item["quantity"]} шт.')
            return redirect(url_for('sales_add'))
    return render_template('sales/add.html', equipment=equipment, categories=categories)

@app.route('/sales/edit/<int:sale_id>', methods=['GET', 'POST'])
def sales_edit(sale_id):
    conn = get_db_connection()
    sale = conn.execute('SELECT * FROM sales WHERE id = ?', (sale_id,)).fetchone()
    equipment = conn.execute('SELECT * FROM equipment').fetchall()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    if request.method == 'POST':
        equipment_id = int(request.form['equipment'])
        category_id = int(request.form['category'])
        date = request.form['date']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        conn.execute('UPDATE sales SET equipment_id=?, category_id=?, date=?, quantity=?, price=? WHERE id=?',
                     (equipment_id, category_id, date, quantity, price, sale_id))
        conn.commit()
        conn.close()
        return redirect(url_for('sales_index'))
    return render_template('sales/edit.html', sale=sale, equipment=equipment, categories=categories)

@app.route('/sales/delete/<int:sale_id>', methods=['GET', 'POST'])
def sales_delete(sale_id):
    if request.method == 'POST':
        code = request.form.get('code')
        if code == os.getenv('DELETE_SECRET'):
            conn = get_db_connection()
            conn.execute('DELETE FROM sales WHERE id = ?', (sale_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('sales_index'))
        else:
            flash('Неверный код удаления')
            return redirect(url_for('sales_delete', sale_id=sale_id))
    return render_template('sales/confirm_delete.html', sale_id=sale_id)

@app.route('/categories')
def categories_index():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('categories/index.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def categories_add():
    if request.method == 'POST':
        name = request.form['name'].strip().lower()  # Normalize name for case-insensitive check
        conn = get_db_connection()
        # Check for duplicate category
        existing = conn.execute('SELECT COUNT(*) FROM categories WHERE LOWER(name) = ?', (name,)).fetchone()[0]
        if existing > 0:
            flash('Категория с таким названием уже существует!')
            conn.close()
            return redirect(url_for('categories_add'))
        # If no duplicate, insert the new category
        conn.execute('INSERT INTO categories (name) VALUES (?)', (request.form['name'],))
        conn.commit()
        conn.close()
        return redirect(url_for('categories_index'))
    return render_template('categories/add.html')

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def categories_edit(category_id):
    conn = get_db_connection()
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        conn.execute('UPDATE categories SET name=? WHERE id=?', (name, category_id))
        conn.commit()
        conn.close()
        return redirect(url_for('categories_index'))
    conn.close()
    return render_template('categories/edit.html', category=category)

@app.route('/categories/delete/<int:category_id>', methods=['GET', 'POST'])
def categories_delete(category_id):
    if request.method == 'POST':
        code = request.form.get('code')
        if code == os.getenv('DELETE_SECRET'):
            conn = get_db_connection()
            equipment_count = conn.execute('SELECT COUNT(*) FROM equipment WHERE category_id = ?', (category_id,)).fetchone()[0]
            sales_count = conn.execute('SELECT COUNT(*) FROM sales WHERE category_id = ?', (category_id,)).fetchone()[0]
            if equipment_count > 0 or sales_count > 0:
                flash('Нельзя удалить категорию, связанную с оборудованием или продажами')
                conn.close()
                return redirect(url_for('categories_delete', category_id=category_id))
            conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('categories_index'))
        else:
            flash('Неверный код удаления')
            return redirect(url_for('categories_delete', category_id=category_id))
    return render_template('categories/confirm_delete.html', category_id=category_id)

# Countries
@app.route('/countries')
@app.route('/countries')
def countries_index():
    """
    Display the list of countries from the database with the number of equipment items linked to each.
    Uses LEFT JOIN to include countries even if they have no equipment yet.
    """
    conn = get_db_connection()
    countries = conn.execute('''
        SELECT c.id, c.name, COUNT(e.id) AS equipment_count
        FROM countries c
        LEFT JOIN equipment e ON c.name = e.country
        GROUP BY c.id, c.name
        ORDER BY c.name
    ''').fetchall()
    conn.close()
    return render_template('countries/index.html', countries=countries)

    """Display list of countries and counts of equipment."""
    conn = get_db_connection()
    countries = conn.execute(
        """
        SELECT c.id, c.name, COUNT(e.id) AS count
        FROM countries c
        LEFT JOIN equipment e ON e.country = c.name
        GROUP BY c.id, c.name
        """)
    conn = get_db_connection()
    countries = conn.execute(
        "SELECT country, COUNT(*) AS count FROM equipment "
        "WHERE country IS NOT NULL AND TRIM(country) <> '' "
        "GROUP BY country"
    ).fetchall()
    conn.close()
    return render_template('countries/index.html', countries=countries)


@app.route('/countries/add', methods=['GET', 'POST'])
def countries_add():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name'].strip()
        if name:
            conn.execute('INSERT INTO countries (name) VALUES (?)', (name,))
            conn.commit()
            conn.close()
            return redirect(url_for('countries_index'))
    conn.close()
    return render_template('countries/add.html')


@app.route('/countries/delete/<int:country_id>', methods=['GET', 'POST'])
def countries_delete(country_id):
    if request.method == 'POST':
        code = request.form.get('code')
        if code == os.getenv('DELETE_SECRET'):
            conn = get_db_connection()
            country = conn.execute('SELECT name FROM countries WHERE id=?', (country_id,)).fetchone()
            if country:
                count = conn.execute('SELECT COUNT(*) FROM equipment WHERE country=?', (country['name'],)).fetchone()[0]
                if count > 0:
                    flash('Нельзя удалить страну, связанную с оборудованием')
                    conn.close()
                    return redirect(url_for('countries_delete', country_id=country_id))
                conn.execute('DELETE FROM countries WHERE id=?', (country_id,))
                conn.commit()
            conn.close()
            return redirect(url_for('countries_index'))
        else:
            flash('Неверный код удаления')
            return redirect(url_for('countries_delete', country_id=country_id))
    return render_template('countries/confirm_delete.html', country_id=country_id)


@app.route('/warehouse')
def warehouse_index():
    conn = get_db_connection()
    items = conn.execute('''
        SELECT e.name AS name, e.quantity, c.name AS category_name 
        FROM equipment e 
        LEFT JOIN categories c ON e.category_id = c.id
    ''').fetchall()
    conn.close()
    return render_template('warehouse/index.html', items=items)

@app.route('/revision')
def revision_index():
    conn = get_db_connection()
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    buy_query = 'SELECT SUM(price * quantity + delivery) FROM equipment'
    sales_count_query = 'SELECT COUNT(*) FROM sales'
    sales_quantity_query = 'SELECT SUM(quantity) FROM sales'
    sales_revenue_query = 'SELECT SUM(price * quantity) FROM sales'

    params = []
    if from_date:
        buy_query += ' WHERE date >= ?'
        sales_count_query += ' WHERE date >= ?'
        sales_quantity_query += ' WHERE date >= ?'
        sales_revenue_query += ' WHERE date >= ?'
        params.append(from_date)
    if to_date:
        buy_query += ' AND' if from_date else ' WHERE'
        sales_count_query += ' AND' if from_date else ' WHERE'
        sales_quantity_query += ' AND' if from_date else ' WHERE'
        sales_revenue_query += ' AND' if from_date else ' WHERE'
        buy_query += ' date <= ?'
        sales_count_query += ' date <= ?'
        sales_quantity_query += ' date <= ?'
        sales_revenue_query += ' date <= ?'
        params.append(to_date)

    total_buy = conn.execute(buy_query, params).fetchone()[0] or 0
    total_sales = conn.execute(sales_count_query, params).fetchone()[0] or 0
    total_quantity_sold = conn.execute(sales_quantity_query, params).fetchone()[0] or 0
    total_sales_revenue = conn.execute(sales_revenue_query, params).fetchone()[0] or 0

    conn.close()
    return render_template('revision/index.html',
                           total_buy=round(total_buy, 2),
                           total_sales=total_sales,
                           total_quantity_sold=total_quantity_sold,
                           total_sales_revenue=round(total_sales_revenue, 2),
                           from_date=from_date,
                           to_date=to_date)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)