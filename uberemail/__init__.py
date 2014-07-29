from flask import Flask
__all__ = ['views']
app = Flask(__name__)

import uberemail.views
