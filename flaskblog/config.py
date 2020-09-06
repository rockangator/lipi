import os


class Config:
    SECRET_KEY = 'bfa078c34cc3af25ddf9aea0d3d9db32'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'greendomicile18@gmail.com'
    MAIL_PASSWORD = 'greendomicile18'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
