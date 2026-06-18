from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'nahid_secret_key_123' 

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'nirob945@nt'

# আসল ডেটা স্টোরেজ (যা পরিবর্তন করা যাবে)
db_settings = {
    "bkash": "017XXXXXXXX",
    "nagad": "019XXXXXXXX"
}

@app.route('/')
def home():
    return render_template('index.html')

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

# ড্যাশবোর্ড এবং পেমেন্ট নম্বর আপডেট করার মেইন লজিক
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # যদি অ্যাডমিন নতুন নম্বর সাবমিট করে (POST Request)
    if request.method == 'POST':
        db_settings['bkash'] = request.form.get('bkash_num')
        db_settings['nagad'] = request.form.get('nagad_num')
        return redirect(url_for('dashboard', page='settings'))

    current_page = request.args.get('page', 'main')
    # টেমপ্লেটে আসল নম্বরগুলো পাঠানো হচ্ছে (data=db_settings)
    return render_template('dashboard.html', current_page=current_page, data=db_settings)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
