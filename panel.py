from flask import Flask, request
import threading
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h2>🚀 ANURAG X AROHI PANEL</h2>
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
    # save uploaded files
    if "tokennum" in request.files:
        request.files["tokennum"].save("tokennum.txt")
    if "file" in request.files:
        request.files["file"].save("File.txt")

    # save text inputs
    open("convo.txt", "w").write(request.form.get("convo", ""))
    open("hatersname.txt", "w").write(request.form.get("hatersname", ""))
    open("time.txt", "w").write(request.form.get("time", "1"))

    # background me main.py run hoga
    def start_main():
        subprocess.Popen(["python", "main.py"])

    threading.Thread(target=start_main).start()

    return "✅ Inputs saved, main.py started in background. Console check karo."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
