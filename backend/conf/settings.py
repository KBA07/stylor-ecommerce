import os


class Config(object):
    SECRET_KEY = os.environ.get('SMTP_SECRET', '1230ab')
    MAIL_SERVER = os.environ.get('SMTP_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('SMTP_PORT', 587)
    MAIL_USE_TLS = os.environ.get('SMTP_VERIFY_TLS', True)
    MAIL_USERNAME = os.environ.get('SMTP_USERNAME', 'arora3mohit@gmail.com')
    MAIL_PASSWORD = os.environ.get('SMTP_PASSWORD')

    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://vidulkumar:New2mlab@ds157493.mlab.com:57493/mydatabase')

    # SOCIAL_FACEBOOK = {
    #     'consumer_key': '2246910702234554',
    #     'consumer_secret': '1724128f42762d9897832bc39cdcd5cf'
    # }
    # MONGO_URI = 'mongodb://vidulkumar:New2mlab@ds157493.mlab.com:57493/mydatabase'
    # #MONGO_URI = "mongodb://localhost:27017/myDatabase"

