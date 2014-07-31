from pprint import pprint as pp
from mailer import Mailer


def build(**kwargs):
  return DummyFailMailer(**kwargs)

class DummyFailMailer(Mailer):
  """Dummy Mailer for unit-testing.

  Always fails to send.
  """
  def __init__(self, **kwargs):
    super(DummyFailMailer, self).__init__(**kwargs)
    self.name = kwargs['name']
  def send(self, **kwargs):
    return False
