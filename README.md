# How to run

```
gunicorn sse:app --worker-class gevent --bind 0.0.0.0:80
```

# how it works?
first go to `/login` and signup/signin to system.

then you will redirected to your dashboard where you can see your contacts.

input name of your friend to send him/her a request.

if he/she approves you, you both will have each others contacts.

click to one of them to open chat messagging window.

start talking!! :)

# features

- login and signup
- add friends to contact
- invite contacts to start a chat powered by webSockets(Socket.io)