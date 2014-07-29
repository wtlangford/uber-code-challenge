from flask import Response, request, render_template
from pprint import (pformat as pf, pprint as pp)
from uberemail import app
import mail

@app.route("/")
def hello():
  return render_template('home.html')

@app.route("/send",methods=["POST"])
def send():
  d = {}
  d["sender"] = request.form["sender"]
  d["to"] = request.form["to"].split(',')
  d["subject"] = request.form["subject"]
  d["text"] = request.form["text"]
  return Response(pf(mail.sendmail(**d)),mimetype="text")
