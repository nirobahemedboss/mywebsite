from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    facebook_url = "https://www.facebook.com/nerobkhan82"
    instagram_url = "https://www.instagram.com/nahid_ahemed_"
    youtube_url = "https://youtube.com/@nahidgaming8"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>নাহিদ আহমেদের ওয়েবসাইট</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #0f172a;
                color: #f8fafc;
                text-align: center;
                padding: 60px 20px;
                margin: 0;
            }}
            .profile-card {{
                max-width: 450px;
                margin: 0 auto;
                background: #1e293b;
                padding: 40px 30px;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
                border: 1px solid #334155;
            }}
            h1 {{
                font-size: 32px;
                margin-bottom: 10px;
                color: #38bdf8;
            }}
            p {{
                color: #94a3b8;
                font-size: 16px;
                margin-bottom: 35px;
            }}
            .btn-container {{
                display: flex;
                flex-direction: column;
                gap: 15px;
            }}
            .btn {{
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 14px;
                font-size: 18px;
                font-weight: bold;
                color: white;
                text-decoration: none;
                border-radius: 12px;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .facebook {{ background-color: #1877F2; }}
            .instagram {{ background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }}
            .youtube {{ background-color: #FF0000; }}
        </style>
    </head>
    <body>

        <div class="profile-card">
            <h1>নাহিদ আহমেদ</h1>
            <p>আমার প্রথম ওয়েবসাইট! নিচে আমার সোশ্যাল মিডিয়া প্রোফাইলগুলো দেওয়া হলো:</p>

            <div class="btn-container">
                <a href="{facebook_url}" target="_blank" class="btn facebook">Facebook পেজ</a>
                <a href="{instagram_url}" target="_blank" class="btn instagram">Instagram প্রোফাইল</a>
                <a href="{youtube_url}" target="_blank" class="btn youtube">YouTube চ্যানেল</a>
            </div>
        </div>

    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)