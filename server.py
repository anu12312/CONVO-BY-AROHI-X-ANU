from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/upload', methods=['POST'])
def upload():
    # Save uploaded files
    if "tokennum" in request.files:
        request.files["tokennum"].save("tokennum.txt")
    if "file" in request.files:
        request.files["file"].save("File.txt")

    # Save text inputs
    open("convo.txt", "w").write(request.form.get("convo", ""))
    open("hatersname.txt", "w").write(request.form.get("hatersname", ""))
    open("time.txt", "w").write(request.form.get("time", "1"))

    # Run main.py
    subprocess.Popen(["python", "main.py"])

    return "✅ Bot started! Check console logs."

if __name__ == "__main__":
    app.run(port=5000, debug=True)
