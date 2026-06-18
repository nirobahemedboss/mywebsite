from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # সেশন সুরক্ষার জন্য যেকোনো একটি সিক্রেট কি দিন

# ডামি ডাটাবেজ (যাতে অ্যাডমিন প্যানেল থেকে ডাটা পরিবর্তন করা যায়)
site_contents = [
    {"id": 1, "title": "প্রথম পোস্ট", "content": "এটি ওয়েবসাইটের প্রথম কনটেন্ট।"},
    {"id": 2, "title": "দ্বিতীয় পোস্ট", "content": "এটি ওয়েবসাইটের দ্বিতীয় কনটেন্ট।"}
]

# অ্যাডমিন লগইন ক্রেডেনশিয়াল
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "nirob945@nt"

@app.route('/')
def home():
    return render_template('dashboard.html', contents=site_contents)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "ভুল ইউজারনেম বা পাসওয়ার্ড!", 401
            
    return '''
        <form method="post" style="max-width:300px; margin:100px auto; font-family:sans-serif;">
            <h2>অ্যাডমিন লগইন</h2>
            <input type="text" name="username" placeholder="ইউজারনেম" required style="width:100%; padding:8px; margin-bottom:10px;"><br>
            <input type="password" name="password" placeholder="পাসওয়ার্ড" required style="width:100%; padding:8px; margin-bottom:10px;"><br>
            <button type="submit" style="width:100%; padding:10px; background:#007bff; color:white; border:none; cursor:pointer;">লগইন</button>
        </form>
    '''

@app.route('/admin')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', contents=site_contents, admin_mode=True)

@app.route('/admin/add', methods=['POST'])
def add_content():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        new_id = len(site_contents) + 1
        site_contents.append({"id": new_id, "title": title, "content": content})
        
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete/<int:content_id>')
def delete_content(content_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    global site_contents
    site_contents = [item for item in site_contents if item['id'] != content_id]
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
