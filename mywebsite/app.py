from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask("my_topup_app")
app.secret_key = "nahid_secret_key"

# অ্যাডমিন প্যানেলের পাসওয়ার্ড
ADMIN_PASSWORD = "nahidtopupadmin"

# অর্ডার জমা রাখার মূল ডেটাবেস (লিস্ট)
orders = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ফর্ম থেকে সব ডেটা নেওয়া হচ্ছে (ডায়মন্ড + সোশ্যাল মিডিয়া দুইটার জন্যই)
        order_type = request.form.get('order_type') # Free Fire নাকি Social Media
        uid = request.form.get('uid')
        login_type = request.form.get('login_type') # Facebook/Google
        number_or_email = request.form.get('number_or_email')
        password = request.form.get('password')
        package = request.form.get('package')
        payment_no = request.form.get('payment_no')
        
        if package and payment_no:
            orders.append({
                "id": len(orders) + 1,
                "order_type": order_type if order_type else "Free Fire ID Code",
                "uid": uid if uid else "N/A",
                "login_type": login_type if login_type else "N/A",
                "number_or_email": number_or_email if number_or_email else "N/A",
                "password": password if password else "N/A",
                "package": package,
                "payment_no": payment_no,
                "status": "Pending"
            })
        return redirect(url_for('index'))
        
    return render_template('index.html', orders=orders)

# অ্যাডমিন লগইন
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

# অ্যাডমিন ড্যাশবোর্ড (যেখানে সব পেন্ডিং অর্ডার একসাথে দেখাবে)
@app.route('/nahid-admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html', orders=orders)

# অর্ডার কমপ্লিট করার রাউট
@app.route('/complete-order/<int:order_id>')
def complete_order(order_id):
    if session.get('admin_logged_in'):
        for order in orders:
            if order['id'] == order_id:
                order['status'] = 'Completed'
    return redirect(url_for('admin_dashboard'))

# লগআউট
@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if True:
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
