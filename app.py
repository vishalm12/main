from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy data for users, items, and admin credentials
users = {'user1': 'password123'}
admin_user = {'admin123': 'admin'}
menu = [
    {'id': 1, 'name': 'Burger', 'price': 50, 'stock': 100},
    {'id': 2, 'name': 'Pizza', 'price': 100, 'stock': 50},
    {'id': 3, 'name': 'Pasta', 'price': 70, 'stock': 200},
    {'id': 4, 'name': 'Coke', 'price': 30, 'stock': 150}
]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        return redirect(url_for('main_menu', username=username))
    flash("Invalid login credentials, please try again.")
    return redirect(url_for('home'))

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    
    if username in admin_user and admin_user[username] == password:
        return redirect(url_for('admin_panel'))
    flash("Invalid admin login credentials, please try again.")
    return redirect(url_for('home'))

@app.route('/main_menu/<username>')
def main_menu(username):
    return render_template('main_menu.html', menu=menu, username=username)

@app.route('/order/<username>/<item_id>', methods=['POST'])
def order(username, item_id):
    quantity = int(request.form['quantity'])
    item = next(item for item in menu if item['id'] == int(item_id))
    
    if item['stock'] >= quantity:
        item['stock'] -= quantity
        total_price = item['price'] * quantity
        return render_template('main_menu.html', menu=menu, username=username, message=f"Order placed! Total: ${total_price}")
    flash("Not enough stock.")
    return redirect(url_for('main_menu', username=username))

@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html', menu=menu)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    item_price = float(request.form['item_price'])
    item_stock = int(request.form['item_stock'])
    
    new_item = {'id': len(menu) + 1, 'name': item_name, 'price': item_price, 'stock': item_stock}
    menu.append(new_item)
    flash(f"Item '{item_name}' added successfully!")
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
