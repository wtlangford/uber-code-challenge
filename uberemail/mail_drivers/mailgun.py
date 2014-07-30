from mailer import Mailer
from pprint import pprint as pp
import requests
from requests.exceptions import ConnectionError, HTTPError

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

  def _sendmail(self, **kwargs):
    try:
# We coerce all of the arguments to the desired types, since they don't
# -necessarily- have to be strings or lists until we send them to the endpoint 
# Don't directly assign kwargs over, as not all of the values will be properly
# keyed
      data={"from": str(kwargs['sender']),
        "to": kwargs['to'],
        "subject": str(kwargs['subject']),
        "text": str(kwargs['text'])
        }
      if 'cc' in kwargs:
        data['cc'] = kwargs['cc']
      if 'bcc' in kwargs:
        data['bcc'] = kwargs['bcc']
      attachments = []
      if 'attachments' in kwargs:
        for attach in kwargs['attachments']:
          print attach
          attachments.append(('attachment',(attach.filename,attach)))
      print "SENDING"
      pp(data)
      pp(attachments)
      pp("{baseURL}/{domain}/messages".format(baseURL=self.baseURL,domain=self.domain))
      r = requests.post("{baseURL}/{domain}/messages".format(baseURL=self.baseURL,domain=self.domain),
          auth=("api",self.key),data=data,files=attachments)
      return r.text
    except ConnectionError:
      return False
    except HTTPError:
      return False
