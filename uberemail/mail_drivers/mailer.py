from pprint import pprint as pp

class Mailer(object):
  """Base class for mail drivers."""

  def __init__(self, **kwargs):
    print "Mailer init: " + kwargs['name']

  def isup(self):
    """Return whether or not this service is currently active and available."""
    return False

  def send(self, **kwargs):
    """Send a message.

    Keyword arguments:
    sender -- email address of the sender
    to -- email address(es) of the recipient(s)
    subject -- subject line
    text -- body of the email
    """
    return None
