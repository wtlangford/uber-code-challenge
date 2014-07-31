from mailer import Mailer
import json
import requests
from requests.exceptions import ConnectionError, HTTPError
from base64 import b64encode
from ..exceptions import MailError #grab this from above.

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
      message = {"from_email": str(kwargs['sender']),
                 "to": [{"email": str(x)} for x in kwargs['to']],
                 "subject": str(kwargs['subject']),
                 "text": str(kwargs['text'])
                }
      if 'cc' in kwargs:
        message['to'].append([{'email': str(x), 'type':'cc'} for x in kwargs['cc']])
      if 'bcc' in kwargs:
        message['to'].append([{'email': str(x), 'type':'bcc'} for x in kwargs['bcc']])
      if 'attachments' in kwargs:
        attachments = []
        for attach in kwargs['attachments']:
          dat = None
          if isinstance(attach['data'], basestring):
            dat = attach['data']
          else:
            dat = attach['data'].read()
          attachments.append({'type': attach['mimetype'],
                              'name': attach['filename'],
                              'content': b64encode(dat)})
        message['attachments'] = attachments
      data = {"key": self.key,"message": message}
      r = requests.post("{baseURL}/messages/send.json".format(baseURL=self.baseURL),
        data=json.dumps(data))
# Right now, we don't funnel data back about if the email failed to send, only 
# if the email can't have sent (because the service didn't like the request)
      if r.status_code != 200:
        result = r.json()
        if result['name'] == 'ValidationError':
          err = json.loads(result['message'][18:])
          if err['message'].keys()[0] == 'from_email':
            raise MailError("Invalid parameter 'sender'.", MailError.InvalidParameter)
          else:
            raise MailError("Unknown validation error. " + pf(err),MailError.InvalidParameter)
      print r.text
      return r.status_code == 200
    except ConnectionError, e:
      return False
    except HTTPError, e:
      return False
