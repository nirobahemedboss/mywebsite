from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_for_diamonds"

# ডেমো ডাটা (ডাটাবেজ ছাড়া সাময়িক সেভের জন্য)
products = {
    "diamond": {"name": "Free Fire Diamond", "price": "৮০", "note": "ইন-গেম অথবা ইউআইডি টপ-আপ"},
    "apps": {"name": "Premium Apps", "price": "৫০", "note": "Netflix, Spotify, Canva, etc."}
}

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # আপনার সিকিউর ইউজারনেম ও পাসওয়ার্ড
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "ভুল পাসওয়ার্ড বা ইউজারনেম! আবার চেষ্টা করুন।"
    return render_template('login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        # অ্যাডমিন প্যানেল থেকে দাম আপডেট করার লজিক
        products['diamond']['price'] = request.form.get('diamond_price')
        products['diamond']['note'] = request.form.get('diamond_note')
        products['apps']['price'] = request.form.get('apps_price')
        products['apps']['note'] = request.form.get('apps_note')
        return redirect(url_for('home'))
        
    return render_template('dashboard.html', products=products)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
