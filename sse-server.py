from flask import Flask, Response, render_template, request
from mongoengine import *
import uuid
from time import sleep
import datetime


app = Flask(__name__)
app.secret_key = 'any random string'
connect('tanishly')
# MODELS
class User(Document):
    id = uuid.uuid4().hex
    username = StringField()
    password = StringField()
    contacts = ListField(StringField())

    # def __init__(self, username, password):
    #     self.username = username
    #     self.password = password

    def append_friend(self,p):
        self.contacts.append(str(p.id))

class Call(Document):
    caller = ReferenceField(User)
    callee = ReferenceField(User)


class StatusLog(Document):
    user = ReferenceField(User)
    sdp = StringField()
    status = StringField(choices=['connect', 'disconnect'])
    time = DateTimeField(default=datetime.datetime.utcnow)





@app.route("/home")
def home():
    u = User("mohsen1","pass1")
    u2 = User("mohsen2", "pass2")
    u2.save()
    u.append_friend(u2)
    u.save()


    return render_template("index.html")


@app.route("/signup", methods=['POST'])
def signup():
    
    try:
        u = User(request.form['username'],
            request.form['password'])
        u.save()
    except e:
        return str(e)

    return "OK"

@app.route("/login", methods=['POST'])
def login():
    u = User.objects(username=request.form['username'],
                password=request.form['password']).first()
    if u:
        session['username'] = u.username
        return "OK"
    return "FALSE"

@app.route("/online")
def online_me():
    u = User.objects(username=session['username']).first()
    
    


@app.route("/stream")
def stream_sse():
    def eventStream():
        while True:
            sleep(2)
            yield "data: {}\n\n".format("hello")
            # Poll data from the database
            # and see if there's a new message
            messages="aaa"
            previous_messages = "a"
            if len(messages) > len(previous_messages):
                yield "data: {}\n\n".format(messages[len(messages)-1])
    
    return Response(eventStream(), mimetype="text/event-stream")

@app.route("/upload", methods=['POST'])
def xhr_server():
    print(request.data)
    return "ok"


@app.route("/p2p")
def p2p():
    return render_template("indexp2p.html")

if __name__=="__main__":
    app.run(debug=True)