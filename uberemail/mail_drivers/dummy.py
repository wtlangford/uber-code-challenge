from pprint import pprint as pp
from mailer import Mailer


def build(**kwargs):
  return DummyMailer(**kwargs)

class DummyMailer(Mailer):
  def __init__(self, **kwargs):
    super(DummyMailer, self).__init__(**kwargs)
    self.name = kwargs['name']
  def isup(self):
    return True
  def send(self, **kwargs):
    print "Dummy send"
    return "Dummy send"
