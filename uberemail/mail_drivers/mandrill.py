from mailer import Mailer
from pprint import pprint as pp
import json
import requests

def build(**kwargs):
  return MandrillMailer(**kwargs)

class MandrillMailer(Mailer):
  def __init__(self, **kwargs):
    super(MandrillMailer, self).__init__(**kwargs)
    self.baseURL = "https://mandrillapp.com/api/1.0"
    self.name = kwargs['name']
    self.key = kwargs['api-key']

  def isup(self):
    return True

  def send(self, **kwargs):
    try:
      assert("sender" in kwargs)
      assert("to" in kwargs)
      assert("subject" in kwargs)
      assert("text" in kwargs)
      data ={"key": self.key,
          "message": {
            "from_email": str(kwargs['sender']),
            "to": [{"email": str(x)} for x in kwargs['to']],
            "subject": str(kwargs['subject']),
            "text": str(kwargs['text'])}} 
      pp(data)
      r = requests.post("{baseURL}/messages/send.json".format(baseURL=self.baseURL),
        data=json.dumps(data))
# We coerce all of the arguments to the desired types, since they don't
# -necessarily- have to be strings or lists until we send them to the endpoint 
      return r.text
    except AssertionError, e:
      return None
