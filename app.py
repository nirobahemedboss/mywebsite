from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'nahid_secret_key_123' 

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'nirob945@nt'

# ডেটাবেজ স্টোরেজ (মেমোরি)
db_settings = {
    "bkash": "01314547049",
    "nagad": "01314547049"
}

# কাস্টমারদের অর্ডার জমা রাখার আসল লিস্ট
orders_db = [
    {"id": 1, "uid": "284719472", "package": "115 Diamonds (85 ৳)", "payment": "0171X-TxnID", "status": "Pending"},
    {"id": 2, "uid": "938401923", "package": "Weekly Pass (160 ৳)", "payment": "0191X-TxnID", "status": "Completed"}
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # হোম পেজের ফর্ম থেকে কাস্টমারের অর্ডার নেওয়া হচ্ছে
        uid = request.form.get('uid')
        package_name = request.form.get('package_name')
        payment_no = request.form.get('payment_no')
        
        # নতুন অর্ডার লিস্টে যোগ করা হচ্ছে
        new_order = {
            "id": len(orders_db) + 1,
            "uid": uid,
            "package": package_name,
            "payment": payment_no,
            "status": "Pending"
        }
        orders_db.insert(0, new_order) # নতুন অর্ডার একদম উপরে দেখাবে
        return render_template('index.html', success="আপনার অর্ডারটি সফলভাবে সাবমিট হয়েছে!", orders=orders_db, data=db_settings)
        
    return render_template('index.html', orders=orders_db, data=db_settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard', page='main'))
        else:
            error = "ভুল পাসওয়ার্ড বা ইউজারনেম!"
            
    return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # অ্যাডমিন প্যানেল থেকে বিকাশ/নগদ নম্বর পরিবর্তন
        db_settings['bkash'] = request.form.get('bkash_num')
        db_settings['nagad'] = request.form.get('nagad_num')
        return redirect(url_for('dashboard', page='settings'))

    current_page = request.args.get('page', 'main')
    
    # স্ট্যাটাস পরিবর্তন করার লজিক (Pending -> Completed)
    action = request.args.get('action')
    order_id = request.args.get('order_id')
    if action and order_id:
        for order in orders_db:
            if order['id'] == int(order_id):
                order['status'] = 'Completed' if action == 'complete' else 'Pending'
        return redirect(url_for('dashboard', page=current_page))

    return render_template('dashboard.html', current_page=current_page, data=db_settings, orders=orders_db)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
