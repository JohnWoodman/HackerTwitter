import os

class Config(object):
    SECRET_KEY = "your-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TWITTER_OAUTH_CLIENT_KEY = "your-api-key"
    TWITTER_OAUTH_CLIENT_SECRET = "your-api-secret"
    
