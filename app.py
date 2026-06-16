from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secret_key_for_md_workspace"

# আপনার নাম্বার ও সোশ্যাল লিংকসহ নতুন ডাটাবেজ
site_data = {
    "title": "Md's Diamond & Premium App Store",
    "notice": "১০০% ট্রাস্টেড এবং সবচেয়ে কম দামে প্রিমিয়াম অ্যাপ ও ডায়মন্ড টপ-আপ কিনুন!",
    "bkash": "01961888782",
    "nagad": "01961888782",
    "rocket": "01961888782",
    "fb_link": "https://www.facebook.com/nerobkhan82",
    "yt_link": "https://youtube.com/@nahidgaming8",
    "telegram_link": "https://www.instagram.com/nahid_ahemed_",
    "products": {
        "diamond": {
            "name": "ফ্রি ফায়ার ডায়মন্ড",
            "price": "৮০",
            "note": "ইন-গেম অথবা ইউআইডি টপ-আপ"
        },
        "apps": {
            "name": "প্রিমিয়াম অ্যাপ",
            "price": "৫০",
            "note": "Netflix, Spotify, Canva, etc."
        }
    }
}

orders = []

@app.route('/')
def home():
    return render_template('index.html', data=site_data)

@app.route('/order', methods=['POST'])
def place_order():
    product_name = request.form.get('product_name')
    game_uid = request.form.get('game_uid')
    payment_method = request.form.get('payment_method')
    sender_number = request.form.get('sender_number')
    txid = request.form.get('txid')
    
    new_order = {
        "id": len(orders) + 1,
        "product": product_name,
        "uid": game_uid if game_uid else "N/A",
        "method": payment_method,
        "sender": sender_number,
        "txid": txid,
        "status": "Pending"
    }
    orders.append(new_order)
    return "<h1>অর্ডার সফল হয়েছে! আমরা কিছুক্ষণের মধ্যে ভেরিফাই করে ডেলিভারি দেব। ধন্যবাদ!</h1><br><a href='/'>হোমপেজে ফিরুন</a>"

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return "ভুল ইউজারনেম বা পাসওয়ার্ড! আবার চেষ্টা করুন।"
    return '''
    <body style="background-color: #0f172a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <form method="post" style="background: #1e293b; padding: 30px; border-radius: 10px; width: 300px; text-align: center; border: 1px solid #334155;">
            <h2>Admin Login Panel</h2>
            <input type="text" name="username" placeholder="Username" required style="width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #475569; background: #0f172a; color: white;"><br>
            <input type="password" name="password" placeholder="Password" required style="width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #475569; background: #0f172a; color: white;"><br>
            <button type="submit" style="background: #d946ef; color: white; border: none; padding: 10px; width: 95%; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px;">লগইন করুন</button>
        </form>
    </body>
    '''

@app.route('/admin/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('dashboard.html', data=site_data, orders=orders)

@app.route('/admin/update', methods=['POST'])
def update_data():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    site_data['title'] = request.form.get('title')
    site_data['notice'] = request.form.get('notice')
    site_data['bkash'] = request.form.get('bkash')
    site_data['nagad'] = request.form.get('nagad')
    site_data['rocket'] = request.form.get('rocket')
    site_data['fb_link'] = request.form.get('fb_link')
    site_data['yt_link'] = request.form.get('yt_link')
    site_data['telegram_link'] = request.form.get('telegram_link')
    
    site_data['products']['diamond']['name'] = request.form.get('diamond_name')
    site_data['products']['diamond']['price'] = request.form.get('diamond_price')
    site_data['products']['diamond']['note'] = request.form.get('diamond_note')
    
    site_data['products']['apps']['name'] = request.form.get('apps_name')
    site_data['products']['apps']['price'] = request.form.get('apps_price')
    site_data['products']['apps']['note'] = request.form.get('apps_note')
    
    return redirect(url_for('dashboard'))

@app.route('/admin/order/complete/<int:order_id>')
def complete_order(order_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'Completed'
            break
    return redirect(url_for('dashboard'))

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
