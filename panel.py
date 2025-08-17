from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>ANURAG X AROHI PANEL</title>
  <style>
    body { font-family: Arial, sans-serif; background: #111; color: #eee; text-align: center; padding: 40px; }
    h2 { color: #0f0; }
    button {
      padding: 12px 20px;
      background: #0f0;
      color: #111;
      border: none;
      border-radius: 8px;
      font-size: 18px;
      cursor: pointer;
    }
    button:hover { background: #1f1; }
    .msg { margin-top: 20px; font-size: 18px; }
  </style>
</head>
<body>
  <h2>🚀 ANURAG X AROHI Control Panel</h2>
  <form method="POST">
    <button type="submit" name="action" value="run">▶ Run main.py</button>
  </form>
  {% if message %}
    <div class="msg">{{ message }}</div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        if request.form.get("action") == "run":
            # background me main.py run karega
            subprocess.Popen(["python", "main.py"])
            message = "✅ main.py started successfully!"
    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
