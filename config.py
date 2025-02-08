import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fee69ceb6dbe67e1c00d287af88d30f3c30e3db78f964f307b791f3a691826d9'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # You can change this to your desired database
    MAIL_SERVER = 'smtp.gmail.com'  # Or use your SMTP provider (e.g., Gmail, AWS SES)
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'wpitts@gmail.com'
