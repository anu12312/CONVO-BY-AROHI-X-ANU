from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>ANURAG X AROHI PANEL</title>
</head>
<body style="text-align:center; font-family:Arial; background:#111; color:#0f0;">
    <h1>🔥 ANURAG X AROHI PANEL 🔥</h1>
    <form action="/run" method="post" enctype="multipart/form-data">
        <p style="font-size:18px">Upload Tokens File:</p>
        <input type="file" name="tokennum"><br><br>

        <p style="font-size:18px">Upload Messages File:</p>
        <input type="file" name="file"><br><br>

        <p style="font-size:18px">Convo ID:</p>
        <input type="text" name="convo"><br><br>

        <p style="font-size:18px">Haters Name:</p>
        <input type="text" name="hatersname"><br><br>

        <p style="font-size:18px">Time (seconds):</p>
        <input type="number" name="time"><br><br>

        <button style="padding:15px; font-size:18px; background:#0f0; border:none; cursor:pointer;">RUN 🚀</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/run", methods=["POST"])
def run_script():
    # uploaded files save karna
    if "tokennum" in request.files:
        request.files["tokennum"].save("tokennum.txt")
    if "file" in request.files:
        request.files["file"].save("File.txt")

    # text inputs save karna
    open("convo.txt", "w").write(request.form.get("convo", ""))
    open("hatersname.txt", "w").write(request.form.get("hatersname", ""))
    open("time.txt", "w").write(request.form.get("time", "1"))

    # ab main.py start karega
    subprocess.Popen(["python", "main.py"])
    return "<h2>✅ Files uploaded & main.py started successfully!</h2><a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
