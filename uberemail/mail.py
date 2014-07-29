import yaml
import importlib
__all__ = ['sendmail']
__drivers = []

def __load_mail_drivers():
  """Load all mail drivers for use."""
  _conf = []
  with open("config/mail.yml","r") as cfgfile:
    cfg = yaml.load(cfgfile)
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

  Keyword arguments:
  sender -- display name and email address of the sender of the email
  to -- email address(es) to which to send the email
  subject -- subject line of the email
  text -- body of the email
  """
  print kwargs 
  for driver in __drivers:
    if (driver.isup()):
      return driver.send(**kwargs)





# When the file is loaded, initialize the drivers.
try:
  __drivers = __load_mail_drivers()
except IOError, err:
  print "Failed to load config.  No mail services available."
except Exception, e:
  print e

