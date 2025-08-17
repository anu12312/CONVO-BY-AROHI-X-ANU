import os
import subprocess
import threading
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h2>ANURAG X AROHI PANEL</h2>
    <form action="/run" method="post" enctype="multipart/form-data">
      Tokens File: <input type="file" name="tokennum"><br><br>
      Convo ID: <input type="text" name="convo"><br><br>
      Messages File: <input type="file" name="file"><br><br>
      Haters Name: <input type="text" name="hatersname"><br><br>
      Time (seconds): <input type="number" name="time"><br><br>
      <button type="submit">RUN</button>
    </form>
    """

@app.route('/run', methods=['POST'])
def run_bot():
    # Save uploaded files
    if "tokennum" in request.files:
        request.files["tokennum"].save("tokennum.txt")
    if "file" in request.files:
        request.files["file"].save("File.txt")

    # Save text inputs
    open("convo.txt", "w").write(request.form.get("convo", ""))
    open("hatersname.txt", "w").write(request.form.get("hatersname", ""))
    open("time.txt", "w").write(request.form.get("time", "1"))

    # Run main.py in background thread
    def run_script():
        subprocess.Popen(["python", "main.py"])

    threading.Thread(target=run_script).start()

    return "✅ Inputs saved, main.py started in background."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Render/Heroku needs 0.0.0.0 + $PORT
    app.run(host="0.0.0.0", port=port)
