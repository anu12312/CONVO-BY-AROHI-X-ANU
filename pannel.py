from flask import Flask, request, render_template_string
import subprocess
import threading
import os

app = Flask(__name__)

# Simple HTML UI
html_page = """
<h2>🔥 ANURAG X AROHI CONTROL PANEL 🔥</h2>
<form action="/run" method="post" enctype="multipart/form-data">
  <label>Upload Token File:</label><br>
  <input type="file" name="tokennum"><br><br>

  <label>Upload Messages File:</label><br>
  <input type="file" name="file"><br><br>

  <label>Convo ID:</label><br>
  <input type="text" name="convo"><br><br>

  <label>Haters Name:</label><br>
  <input type="text" name="hatersname"><br><br>

  <label>Time (seconds):</label><br>
  <input type="number" name="time" value="1"><br><br>

  <button type="submit">🚀 RUN</button>
</form>
"""

@app.route('/')
def index():
    return render_template_string(html_page)

@app.route('/run', methods=['POST'])
def run_bot():
    # Save token file
    if "tokennum" in request.files:
        request.files["tokennum"].save("tokennum.txt")

    # Save message file
    if "file" in request.files:
        request.files["file"].save("File.txt")

    # Save convo id, hatersname, time
    open("convo.txt", "w").write(request.form.get("convo", ""))
    open("hatersname.txt", "w").write(request.form.get("hatersname", ""))
    open("time.txt", "w").write(request.form.get("time", "1"))

    # Run main.py in background
    def run_script():
        subprocess.run(["python", "main.py"], shell=False)

    threading.Thread(target=run_script).start()

    return "✅ Files saved and main.py started! Console dekh."

if __name__ == '__main__':
    print("🚀 Panel chalu ho gaya: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
