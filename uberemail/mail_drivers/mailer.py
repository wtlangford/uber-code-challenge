from pprint import pprint as pp

class Mailer(object):
  def __init__(self, **kwargs):
    print "Mailer init: " + kwargs['name']
  def isup(self):
    return False
  def send(self, **kwargs):
    return None
