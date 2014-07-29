from flask import Response, request, render_template
import json
from pprint import (pformat as pf, pprint as pp)
from uberemail import app
import mail

@app.route("/")
def hello():
  return render_template('home.html')

@app.route("/send",methods=["POST"])
def send():
  d = {'sender': request.form['sender'],
       'to': request.form['to'].split(','),
       'subject': request.form['subject'],
       'text': request.form['text'],
      }
  return Response(json.dumps(mail.sendmail(**d)), mimetype="application/json")
