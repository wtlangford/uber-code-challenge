
class Mailer(object):
  """Base class for mail drivers."""

  def __init__(self, **kwargs):
    print "Mailer init: " + kwargs['name']

  def _sendmail(self, **kwargs):
    """Overload this in all subclasses."""
    return False

  def send(self, **kwargs):
    """Send a message.

    Keyword arguments:
    sender -- email address of the sender
    to -- email address(es) of the recipient(s)
    subject -- subject line
    text -- body of the email
    """
    try:
      assert("sender" in kwargs)
      assert("to" in kwargs)
      assert("subject" in kwargs)
      assert("text" in kwargs)
      return self._sendmail(**kwargs)
    except AssertionError, e:
      return False
