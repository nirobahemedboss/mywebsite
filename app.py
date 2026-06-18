from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ১. হোম পেজ (index.html) রেন্ডার করার জন্য
@app.route('/')
def home():
    return render_template('index.html')

# ২. লগইন পেজ (login.html) রেন্ডার করার জন্য
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # এখানে লগইন লজিক থাকবে (আপাতত সরাসরি ড্যাশবোর্ডে পাঠিয়ে দেওয়া হচ্ছে)
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# ৩. ড্যাশবোর্ড পেজ (dashboard.html) রেন্ডার করার জন্য
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
