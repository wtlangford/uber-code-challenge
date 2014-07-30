from mailer import Mailer
from pprint import pprint as pp
import json
import requests
from requests.exceptions import ConnectionError, HTTPError

def build(**kwargs):
  return MandrillMailer(**kwargs)

class MandrillMailer(Mailer):
  """Mandrill mailer.

  Settings for configuration file:
  api-key -- Mandrill api key
  """

  def __init__(self, **kwargs):
    super(MandrillMailer, self).__init__(**kwargs)
    self.baseURL = "https://mandrillapp.com/api/1.0"
    self.name = kwargs['name']
    self.key = kwargs['api-key']


  def _sendmail(self, **kwargs):
    try:
# We coerce all of the arguments to the desired types, since they don't
# -necessarily- have to be strings or lists until we send them to the endpoint 
      data = {"key": self.key,
              "message": {
                "from_email": str(kwargs['sender']),
                "to": [{"email": str(x)} for x in kwargs['to']],
                "subject": str(kwargs['subject']),
                "text": str(kwargs['text'])
              }
             } 
      pp(data)
      r = requests.post("{baseURL}/messages/send.json".format(baseURL=self.baseURL),
        data=json.dumps(data))
      return r.json()
    except ConnectionError, e:
      return False
    except HTTPError, e:
      return False
