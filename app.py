from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'nahid_secret_key_123' 

# আপনার দেওয়া পাসওয়ার্ড
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'nirob945@nt'

@app.route('/')
def home():
    return render_template('index.html')

# লগইন রাউট
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = "ভুল পাসওয়ার্ড বা ইউজারনেম!"
            
    return render_template('login.html', error=error)

# ড্যাশবোর্ড রাউট (সুরক্ষিত)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# লগআউট রাউট
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
