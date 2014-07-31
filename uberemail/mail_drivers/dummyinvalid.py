from pprint import pprint as pp
from mailer import Mailer
from ..exceptions import MailError


def build(**kwargs):
  return DummyInvalidMailer(**kwargs)

class DummyInvalidMailer(Mailer):
  """Dummy Mailer for unit-testing.

  Always raises an invalid parameter error
  """
  def __init__(self, **kwargs):
    super(DummyInvalidMailer, self).__init__(**kwargs)
    self.name = kwargs['name']
  def send(self, **kwargs):
    raise MailError("Dummy Error", MailError.InvalidParameter)
