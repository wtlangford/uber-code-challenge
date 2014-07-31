#!/bin/env python2.7
import subprocess
import json
import requests
from base64 import b64encode
from pprint import pprint as pp
from time import sleep

def init_tests():
  subprocess.call("./start_gunicorn")
  sleep(1)
  subprocess.call(["cp","./config/mail.yml","./config/mail.yml.bkp"])
  

def restart_server():
  subprocess.call("./restart_gunicorn")
  sleep(1)

def teardown_tests():
  subprocess.call(["mv","./config/mail.yml.bkp","./config/mail.yml"])
  restart_server()

def runtest(drivers=[], data="", content_type="application/json"):
  hdr = {}
  if content_type is not None:
    hdr = {'Content-Type':content_type}
  # icky, but simple.  This should be replaced with something better...
  with open("config/mail.yml","w") as outfile:
    subprocess.call(["cat", "test/header.yml"] + ["test/{}.yml".format(x) for x in drivers], stdout=outfile)
  restart_server()

  return requests.post("http://localhost:8000/send",data=data, headers=hdr)

good_email = {
    "sender": "wlangfor@gmail.com",
    "to": "wlangfor@gmail.com",
    "subject": "Test email",
    "text": "Test body",
    }

missing_to = {
    "sender": "wlangfor@gmail.com",
    "subject": "Test email",
    "text": "Test body",
    }

missing_sender = {
    "to": "wlangfor@gmail.com",
    "subject": "Test email",
    "text": "Test body",
    }

invalid_sender = {
    "sender": "wlangfor at gmail.com",
    "to": "wlangfor@gmail.com",
    "subject": "Test email",
    "text": "Test body",
    }

class TestError(Exception):
  def __init__(self, number):
    self.number = number
  def __str__(self):
    return "TestError failed test {}".format(self.number)

def getfiles():
  return {'attachments': [{'filename': 'content1', 'data': b64encode("Content 1!\n"), 'mimetype':'text'}]}

init_tests()
try:

  # Test mailer loading with dummy mailers.
  r = runtest(["dummypass"], json.dumps(good_email))
  if r.status_code != 200:
    raise TestError(1)
  else:
    print "Pass 1"
  r = runtest(["dummyfail"], json.dumps(good_email))
  if r.status_code != 400 and r.json()['error'] != 5:
    raise TestError(2)
  else:
    print "Pass 2"

  # Test fallthrough of failing services
  r = runtest(["dummyfail","dummypass"], json.dumps(good_email))
  if r.status_code != 200:
    raise TestError(3)
  else:
    print "Pass 3"

  # If the service reports the data is bad, we abort.
  r = runtest(["dummyinvalid"], json.dumps(good_email))
  if r.status_code == 200 or r.json()['error'] != 2:
    raise TestError(4)
  else:
    print "Pass 4"

  # Confirm no fallthrough if service reports bad data
  r = runtest(["dummyinvalid","dummypass"], json.dumps(good_email))
  if r.status_code == 200 or r.json()['error'] != 2:
    raise TestError(5)
  else:
    print "Pass 5"

  # Test services
  r = runtest(["mailgun"], json.dumps(good_email))
  if r.status_code != 200:
    raise TestError(6)
  else:
    print "Pass 6"
  r = runtest(["mandrill"], json.dumps(good_email))
  if r.status_code != 200:
    raise TestError(7)
  else:
    print "Pass 7"

  # Test mailgun failure
  r = runtest(["mailgunfail"], json.dumps(good_email))
  if r.status_code == 200 or r.json()['error'] != 5:
    raise TestError(8)
  else:
    print "Pass 8"

  # Test mailgun fallthrough
  r = runtest(["mailgunfail","mandrill"], json.dumps(good_email))
  if r.status_code != 200:
    raise TestError(9)
  else:
    print "Pass 9"

  # Test invalid data
  r = runtest(["mandrill"], json.dumps(missing_sender))
  if r.status_code == 200 or r.json()['error'] != 1:
    raise TestError(10)
  else:
    print "Pass 10"
  r = runtest(["mandrill"], json.dumps(missing_to))
  if r.status_code == 200 or r.json()['error'] != 1:
    raise TestError(11)
  else:
    print "Pass 11"
  r = runtest(["mandrill"], json.dumps(invalid_sender))
  if r.status_code == 200 or r.json()['error'] != 2:
    raise TestError(12)
  else:
    print "Pass 12"


  # Test attachments
  r = runtest(["mailgun"], json.dumps(dict(good_email.items() + getfiles().items())))
  if r.status_code != 200:
    raise TestError(13)
  else:
    print "Pass 13"
  r = runtest(["mandrill"], json.dumps(dict(good_email.items() + getfiles().items())))
  if r.status_code != 200:
    raise TestError(14)
  else:
    print "Pass 14"
except TestError, e:
  print e, r.status_code, r.text
except Exception as e:
  print e
except: # I want to make sure that teardown_tests() is called when Ctrl-C happens...
  pass
finally:
  teardown_tests()

