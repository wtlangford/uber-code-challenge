Readme
======

I chose the Email Service project and the back-end track.

Technical Choices
----
- Written in Python 2
- Uses Flask for the HTTP server
  - Flask was chosen for its light weight and ease of use
- Configuration files are written in yaml
- The requests library is used for all HTTP requests, as urllib2 is just sad.
- gunicorn is used to interface between the application and the internet. In a more serious production environment, gunicorn should be behind an nginx proxy.
- In order to make the service flexible and modular, the connections to the mail servers are loaded dynamically.  When the server starts up, the config file is processed.  Each service listed contains a settings dictionary (to allow multiple instances of the same service to coexist.  Multiple mailgun accounts, perhaps), as well as a module name.


Service Configuration
---------------------
The `config/mail.yml` file looks as follows:

```yaml
drivers:
  - name: "Human-readable service name."
    module: "module_name"
    settings:
      setting1: "value1"
      setting2: "value2"
  - name: "Human-readable service name 2."
    module: "module_name2"
    settings:
      setting1: "value1"
      setting2: "value2"
```
`module` refers to a python module that should be inside of the package `uberemails.mail_drivers`.  The `settings` dictionary is passed directly to the driver's constructor as `**kwargs`

Presently, modifications to the config file requires a restart of the server.


Mail Driver
-----------
All mail drivers inherit from `uberemail.mail_drivers.mailer.Mailer`.
There is one method to be overridden when new drivers are added.
`_sendmail(self,**kwargs)` is called from `Mailer` when mail is to be sent.
It expects the following args to be passd in:
- `sender`: email address of the sender
- `to`: email address of the recipient or a list of email addresses.
- `subject`: subject line of the email
- `text`: textual body of the email

It also recognizes the following optional arguments:
- `cc`, `bcc`: email address(es). May be a single email or a list of emails.
- `attachments`: Files to be attached.  This should be a list of dictionaries.  Each dictionary has the following keys:
  - `filename`: filename of the attachment
  - `data`: data for the attachment.  May be either a string or a `file`-like object.
  - `mimetype`: mimetype of the attachment.

If the mail is sent successfully, then `_sendmail` is to return `True`.  If the service is not currently available/working, `_sendmail` is to return `False`.  If the service reports that the data is invalid, `_sendmail` is to raise a `MailError`.


MailError
---------
`MailError` is the exception class used to signal various errors and propagate them back to the API's response.  It lives in `uberemail.exceptions` and has a few error codes that get passed back to the user in the response JSON.


Sending Emails
--------------
Emails can be sent with the service by sending a `POST` request containing JSON to `/send`.  The `Content-Type` should be set to `application/json`.  The service also tentatively accepts `multipart/form-data` and `application/x-www-form-urlencoded` content types, but these are presently unreliable.

The JSON message sent to the server should look like this:
```json
{
  sender: "sender@sample.com",
  to: "recipient@sample.com",
  subject: "Subject line",
  text: "Body of the email..."
}
```
It also optionally supports `cc`, `bcc`, and `attachments`.
Once again, `to`, `cc`, and `bcc` support multiple addresses.
`attachments` is a list of dictionaries.  The only required entry is the data, which is to be a base-64 encoded string.
```json
{
  sender: "sender@sample.com",
  to: "recipient@sample.com",
  bc: ["cc1@sample.com", "cc2@sample.com"],
  bcc: ["bcc@sample.com"],
  subject: "Subject line",
  text: "Body of the email..."
  attachments: [
    {
      filename: "filename"
      data: "base64-encoded data",
      mimetype: "mimetype"
    },
    {
      data: "base64-encoded data 2"
    }
  ]
}
```

If using `multipart/form-data` or `application/x-www-form-urlencoded`, `to`, `cc`, and `bcc` may be either a comma-separated list of email addresses or appear multiple times in the form data.


Testing
-------

Testing is done by running `tests.py` in the main directory.  It will launch and control gunicorn using the `start_gunicorn`, `stop_gunicorn`, and `restart_gunicorn` scripts.

Currently the testing code is very repetitive.  It needs to be reworked such that one can just add functions that get called instead of manually writing each test.


Additional Thoughts
-------------------
Things that should be changed if I were to spend more time on this:
 - Be more responsive to changes to the configuration.  Possibly change to loading all `.yml` files in the `config/` folder.
 - Improve testing code
 - Fix the wonkiness in `application/x-www-form-urlencode` and `multipart/form-data` code


Resume
------
My resume can be found [here](http://wlangford.net/resume.pdf)

My github is [@wtlangford](http://github.com/wtlangford)













