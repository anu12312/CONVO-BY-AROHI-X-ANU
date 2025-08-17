from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_main():
    data = request.form

    # form से values लेके txt files में save करो
    with open("tokennum.txt", "w") as f:
        f.write(data.get("token", ""))

    with open("convo.txt", "w") as f:
        f.write(data.get("convo", ""))

    with open("hatersname.txt", "w") as f:
        f.write(data.get("hater", ""))

    with open("time.txt", "w") as f:
        f.write(data.get("time", "1"))

    # message file save करना
    file = request.files.get("file")
    if file:
        file.save("File.txt")

    # अब main.py run करो
    subprocess.Popen(["python", "main.py"])

    return jsonify({"message": "✅ main.py started!"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
