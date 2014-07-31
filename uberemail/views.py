from flask import Response, request, render_template
import json
from uberemail import app
import mail
from base64 import b64decode
from exceptions import MailError


@app.route("/")
def hello():
  return render_template('home.html')

@app.route("/send",methods=["POST"])
def send():
  try:
    d = {}
    args = None
    # Would use request.is_json, but not available in flask < 0.11 D:
    if request.mimetype in ['application/json','application/*+json']:
      args = request.get_json(silent=True)
      if args is None:
        raise MailError("Invalid JSON", MailError.InvalidJSON)
      atts = []
      if 'attachments' in args:
        for atch in args['attachments']:
          if 'data' not in atch:
            raise MailError("'data' required for attachments.", MailError.InvalidParameter)
          atch['data'] = b64decode(atch['data'])
          if 'filename' not in atch:
            atch['filename'] = ''
          if 'mimetype' not in atch:
            atch['mimetype'] = ''
          atts.append(atch)
        d['attachments'] = atts
    elif request.mimetype in ['multipart/form-data', 'application/x-www-form-urlencoded']:
      # Since we handle json and form inputs together below,
      # roll duplicate keys into an array.
      args = {}
      for key,val in request.form.iterlists():
        if len(val) == 1:
          args[key] = val[0]
        else:
          args[key] = val
        d['attachments'] = [{"filename":atch.filename, "mimetype":atch.mimetype, "data":atch.stream}
                          for atch in request.files.getlist('attachments')]
    else:
      raise MailError(request.mimetype + " not supported.", MailError.InvalidMIMEType)
    for arg in ['sender', 'subject', 'text', 'to']:
      if arg not in args:
        raise MailError("Missing parameter '" + arg + "'", MailError.MissingParameter)
      d.update({'sender': args['sender'],
          'subject': args['subject'],
          'text': args['text'],
         })
    for arg in ['to','cc','bcc']:
      if arg in args:
        # Since form inputs with the multiple attribute will combine these
        # using ',', handle that.  Also support multiple instance of the 
        if isinstance(args[arg], basestring):
          d[arg] = [x for x in args[arg].split(',') if len(x) > 0]
        elif isinstance(args[arg], list):
          d[arg] = [x for x in args[arg] if len(x) > 0]
        else:
          raise MailError("Invalid parameter '" + arg + "'.  Must be array or string", MailError.InvalidParameter)
    if len(args['to']) == 0:
      raise MailError("Missing parameter 'to'.", MailError.MissingParameter);
    return Response(json.dumps(mail.sendmail(**d)),mimetype="application/json")
  except MailError as e:
    return Response(json.dumps({"error": e.errorcode, "message": e.message}),
              mimetype="application/json",
              status=e.httpstatus)
