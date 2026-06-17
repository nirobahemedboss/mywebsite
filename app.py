from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(name)
app.secret_key = "nahid_secret_key" # সিকিউরিটি কি

# অ্যাডমিন প্যানেলের পাসওয়ার্ড (তুমি চাইলে পরিবর্তন করতে পারো)
ADMIN_PASSWORD = "nahidtopupadmin"

# ডেমো ডেটাবেস (অর্ডার জমা রাখার জন্য)
orders = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uid = request.form.get('uid')
        payment_no = request.form.get('payment_no')
        package = request.form.get('diamond_package')
        
        if uid and payment_no and package:
            # নতুন অর্ডার লিস্টে জমা করা
            orders.append({
                "id": len(orders) + 1,
                "uid": uid,
                "payment_no": payment_no,
                "package": package,
                "status": "Pending"
            })
        return redirect(url_for('index'))
        
    return render_template('index.html', orders=orders)

# অ্যাডমিন লগইন রাউট
@app.route('/nahid-admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="ভুল পাসওয়ার্ড!")
    return render_template('admin_login.html')

# অ্যাডমিন ড্যাশবোর্ড রাউট
@app.route('/nahid-admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html', orders=orders)

# অর্ডারের স্ট্যাটাস পরিবর্তন করার রাউট
@app.route('/complete-order/<int:order_id>')
def complete_order(order_id):
    if session.get('admin_logged_in'):
        for order in orders:
            if order['id'] == order_id:
                order['status'] = 'Completed'
    return redirect(url_for('admin_dashboard'))

# লগআউট রাউট
@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if name == 'main':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
