from pprint import pprint as pp
from mailer import Mailer


def build(**kwargs):
  return DummyPassMailer(**kwargs)

class DummyPassMailer(Mailer):
  """Dummy Mailer for unit-testing.

  Always succeeds at sending
  """
  def __init__(self, **kwargs):
    super(DummyPassMailer, self).__init__(**kwargs)
    self.name = kwargs['name']
  def send(self, **kwargs):
    return True
