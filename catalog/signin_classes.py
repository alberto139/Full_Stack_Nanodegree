import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Auth:
    """Google Project Credentials"""
    CLIENT_ID = ('182928969519-esu93t2dgj5hbt87mj1u142cc865flgl.apps.googleusercontent.com')
    CLIENT_SECRET = 'JFhN7REK_HiP-4XEriapEMfY'
    REDIRECT_URI = 'https://localhost:5010/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


class Config:
    """Base config"""
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"


class DevConfig(Config):
    """Dev config"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")


class ProdConfig(Config):
    """Production config"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")