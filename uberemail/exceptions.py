class MailError(Exception):
  MissingParameter = 1
  InvalidParameter = 2
  InvalidJSON      = 3
  InvalidMIMEType  = 4
  NoServicesActive = 5

  def __init__(self, message, errorcode, httpstatus=400):
    self.message = message
    self.errorcode = errorcode
    self.httpstatus = httpstatus
  def __str__(self):
    return json.dumps({"error":self.errorcode, "message":self.message})
