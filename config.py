# config.py: Secret key configuration
import secrets
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
