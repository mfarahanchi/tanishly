from flask import Flask, render_template, flash, request, url_for, redirect, session, abort
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_sse import sse
import random



app = Flask(__name__)
app.config["REDIS_URL"] = 'redis://localhost:6379'
app.register_blueprint(sse, url_prefix='/stream')

socketio = SocketIO(app)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

class User(UserMixin):

    def __init__(self, id,name, password):
        self.id = id
        self.name = name
        self.password = password


user_names = []

@app.route('/')
def index():
    if session['username'] in contacts.keys():
        my_contacts = contacts[session['username']]
    else:
        contacts[session['username']] = []
        my_contacts = []
    return render_template("index.html", contacts=my_contacts)

@app.route('/login' , methods = ['POST','GET'])
def login():
    if request.method == "POST":
        name = request.form['username']
        password = request.form['password']
        if name in user_names: # TODO: query in db
            if not password == password:
                flash("error", "password missmatch, 401")
            else:
                session['username'] = name
                return redirect(url_for('index'))
        else: 
            user_names.append(name)
            # login_user(user)
            flash("info", "user created")
    return render_template("login.html")


@app.route('/contact/<requested>' , methods = ['POST', 'GET'])
def contact(requested):
    if not session['username']:
        abort(401)
    if request.method == "GET":
        # name = request.form['username']
        name = requested
        # if name in user_names:
        if True:
            sse.publish({"message" : "{}".format(session['username'])}, type='new_contact', channel=requested)
            # return "{} added to your contact.".format(name)
        else:
            sse.publish({"message" : "no such user singed! : {}".format(name)}, type='new_contact')
    return render_template("contact.html")


contacts = dict()
contacts['m_farahanchi'] = ['felani']
contacts['felani'] = ['m_farahanchi']

@app.route('/contact/approve/<username>')
def approve_contact(username):
    if not session['username']:
        abort(401)
    print("before")
    print(contacts)
    print("username" + username)
    print("session" + session['username'])
    # if username in contact.keys():
    if True:
        contacts[username].append(session['username'])
        sse.publish({'username': session['username']}, type='added_contact', channel=username)
    if True:
        contacts[session['username']].append(username)
        sse.publish({'username': username}, type='added_contact', channel=session['username'])

    # TODO: add contact session[] to username
    print("after")
    print(contacts)
    return "200"

@app.route('/chat')
def chat_page():
    return render_template("chat.html")

rooms = []

# Socket io Enabled
@app.route('/new_room/<name>')
def new_room(name):
    if not session['username']:
        abort(401)
    # if name is in sessions contacts
    # sse to name and retrive sdp
    sse.publish({"message": "new room created : {}".format(name), "user":session['username']}, type='new_room', channel=name)
    rooms.append(name)
    return "new room created : {}".format(name)

@app.route('/chat/invite/<invitee>', methods=['GET'])
def join_first(invitee):
    sse.publish({"invite": session['username'], 'url': "chat/join/{}".format(session['username'])}, type='invite', channel=invitee)
    return render_template('chat.html',peer=invitee)

@app.route('/chat/join/<party>', methods=['GET'])
def join_second(party):
    if not session['username']:
        abort(401)
    return render_template('chat2.html', peer=party)


@app.route('/p2p')
def p2p():
    return render_template('indexp2p.html')

@socketio.on('join')
def on_join(data):
    username = session['username']
    room = data['room']
    session['room'] = room
    join_room(room)
    print("join {}".format(username))
    send(username + ' has entered the room.', room=room)

@socketio.on('new_message')
def on_new_message(data):
    print(data)
    emit('message', {'username': data['username'],'message': data['message']}, room = session['room'])


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

# @socketio.on('disconnect')
# def on_disconnect(data):
#     username = session['username']
#     room = data['room']
#     leave_room(room)
#     send(username + " disconnected", room = room)
# @app.route('/add_to_room/<room>/<user>')
# def add_to_room(room, user):
#     if room in rooms:
#         sse.publish({"message": "new user {} added to room:{}".format(user, room)}, type='new_user')

#     return "user {} added to room : {}".format(user, room)

