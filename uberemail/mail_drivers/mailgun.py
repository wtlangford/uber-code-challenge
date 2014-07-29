from mailer import Mailer
from pprint import pprint as pp
import requests

def build(**kwargs):
  return MailgunMailer(**kwargs)

class MailgunMailer(Mailer):
  """Mailgun mailer.

  Settings for configuration file:
  domain -- Sending domain (domain from which email is sent)
  api-key -- Mailgun private API key
  """

  def __init__(self, **kwargs):
    super(MailgunMailer, self).__init__(**kwargs)
    self.baseURL = "https://api.mailgun.net/v2"
    self.name = kwargs['name']
    self.key = kwargs['api-key']
    self.domain = kwargs['domain']

  def isup(self):
    return True

  def send(self, **kwargs):
    try:
      assert("sender" in kwargs)
      assert("to" in kwargs)
      assert("subject" in kwargs)
      assert("text" in kwargs)
# We coerce all of the arguments to the desired types, since they don't
# -necessarily- have to be strings or lists until we send them to the endpoint 
      r = requests.post("{baseURL}/{domain}/messages".format(baseURL=self.baseURL,domain=self.domain),
          auth=("api",self.key),
          data={"from": str(kwargs['sender']),
            "to": kwargs['to'],
            "subject": str(kwargs['subject']),
            "text": str(kwargs['text'])})
      return r.json()
    except AssertionError, e:
      return None
