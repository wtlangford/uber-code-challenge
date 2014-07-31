from mailer import Mailer
from pprint import pprint as pp
import requests
from requests.exceptions import ConnectionError, HTTPError
from ..exceptions import MailError

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
          attachments.append(('attachment',(attach['filename'],attach['data'])))
      r = requests.post("{baseURL}/{domain}/messages".format(baseURL=self.baseURL,domain=self.domain),
          auth=("api",self.key),data=data,files=attachments)
      pp(r.status_code)
      if r.status_code == 400:
        msg = r.json()['message']
        param = msg.split("'")[1]
        if param == 'from':
          raise MailError("Invalid parameter 'to'.", MailError.InvalidParameter)
        raise MailError("Invalid parameter " + param, MailError.InvalidParameter)
      elif r.status_code == 200:
        return True
      else:
        print "MailgunMailer: Error:{}: {}".format(r.status_code,r.text) # log it for later.
        return False
    except ConnectionError:
      return False
    except HTTPError:
      return False
