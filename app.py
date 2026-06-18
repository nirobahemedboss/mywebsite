from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask("my_topup_app")
app.secret_key = "nahid_secret_key"

ADMIN_PASSWORD = "nahidtopupadmin"

# Demo database (List)
orders = []

# Prothom-e kichhu default package rekhe dilam jate blank na thake
packages = [
    {
        "id": 1,
        "name": "Free Fire New Top-Up Event",
        "price": 100,
        "image_url": "https://i.ibb.co.co/placeholder1.png", # Apnar original image url boshan
        "tag": "NEW"
    },
    {
        "id": 2,
        "name": "Free Fire Diamond Top Up BD",
        "price": 180,
        "image_url": "https://i.ibb.co.co/placeholder2.png",
        "tag": "HOT"
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uid = request.form.get('uid')
        payment_no = request.form.get('payment_no')
        package = request.form.get('diamond_package')

        if uid and payment_no and package:
            orders.append({
                "id": len(orders) + 1,
                "uid": uid,
                "payment_no": payment_no,
                "package": package,
                "status": "Pending"
            })
            return redirect(url_for('index'))

    # index.html e packages list-o pathiye dilam
    return render_template('index.html', orders=orders, packages=packages)

@app.route('/nahid-admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error="Bhul Password!")
    return render_template('login.html')

@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Jodi admin dashboard theke noutun package push kora hoy
    if request.method == 'POST':
        package_name = request.form.get('package_name')
        package_price = request.form.get('package_price')
        package_image = request.form.get('package_image')
        package_tag = request.form.get('package_tag')

        if package_name and package_price:
            packages.append({
                "id": len(packages) + 1,
                "name": package_name,
                "price": int(package_price),
                "image_url": package_image if package_image else "https://placehold.co/600x400",
                "tag": package_tag
            })
            return redirect(url_for('admin_dashboard'))

    return render_template('dashboard.html', orders=orders)

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# Order complete korar jonno route
@app.route('/complete-order/<int:order_id>')
def complete_order(order_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'Done'
            break
    return redirect(url_for('admin_dashboard'))
