from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Control Panel</title>
</head>
<body>
  <h2>ANURAG X AROHI Control Panel</h2>
  <form method="POST">
    <button type="submit" name="action" value="run">Run Script</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("action") == "run":
            subprocess.Popen(["python", "main.py"])
            return "<p>✅ Script started!</p><a href='/'>Back</a>"
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
