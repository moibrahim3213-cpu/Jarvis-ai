
# JARVIS WEB AI - FINAL (ONE FILE)
# Run:
#   pip install flask
#   python jarvis_web.py

from flask import Flask,request,render_template_string
import datetime,json,os

app = Flask(__name__)
MEMORY_FILE="jarvis_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE))
    return {}

def save_memory(mem):
    json.dump(mem,open(MEMORY_FILE,"w"),indent=2)

memory=load_memory()

def brain(text):
    t=text.lower()
    if "time" in t:
        return datetime.datetime.now().strftime("Time: %H:%M:%S")
    if "date" in t:
        return datetime.datetime.now().strftime("Date: %Y-%m-%d")
    if t.startswith("remember"):
        memory["note"]=t.replace("remember","").strip()
        save_memory(memory)
        return "Saved to memory."
    if "what do you remember" in t:
        return str(memory)
    return "JARVIS online."

HTML="""
<html>
<head>
<title>JARVIS</title>
<style>
body{background:#0b1c2d;color:#00eaff;font-family:Consolas}
</style>
</head>
<body>
<h1>JARVIS</h1>
<form method="post">
<select name="mode">
<option>Keyboard</option>
<option>Hands</option>
<option>Face</option>
<option>Hands+Face</option>
</select><br><br>
<input name="msg" placeholder="Talk to JARVIS">
<button>Send</button>
</form>
<p>{{reply}}</p>
</body>
</html>
"""

@app.route("/",methods=["GET","POST"])
def home():
    reply=""
    if request.method=="POST":
        reply=brain(request.form["msg"])
    return render_template_string(HTML,reply=reply)

app.run()
