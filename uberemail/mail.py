import yaml
import importlib
from exceptions import MailError
__all__ = ['sendmail']
__drivers = []

def __load_mail_drivers():
  """Load all mail drivers for use."""
  _conf = []
  with open("config/mail.yml","r") as cfgfile:
    cfg = yaml.load(cfgfile)
    if cfg is None or cfg["drivers"] is None:
      return []
    for driver_cfg in cfg["drivers"]:
      try:
        driver_mod = importlib.import_module(".mail_drivers."+driver_cfg["module"], __package__)
        _conf.append(driver_mod.build(name=driver_cfg['name'], **driver_cfg['settings']))
      except Exception, e:
        print "Failed to load {0}.".format(driver_cfg['name']), e
    return _conf

def sendmail(**kwargs):
  """Sends an email using the first available service.

  Services are used in the order in which they are listed
  in the configuration file.

  Required keyword arguments:
  sender -- email address of the sender
  to -- email address(es) of the recipients
  subject -- subject line of the email
  text -- body of the email

  Optional keyword arguments:
  cc -- email address(es) of the cc recipients
  bcc -- email address(es) of the bcc recipients
  attachments -- array of dict("filename", "mimetype", "data").  Data is to be
    like a file object.
  """
  print kwargs 
# Attempt sending for each currently active driver.
  for driver in __drivers:
    success = driver.send(**kwargs)
    if success:
      return success
  raise MailError("No services able to send email.", MailError.NoServicesActive)





# When the file is loaded, initialize the drivers.
try:
  __drivers = __load_mail_drivers()
except IOError, err:
  print "Failed to load config.  No mail services available."
except Exception, e:
  print e

