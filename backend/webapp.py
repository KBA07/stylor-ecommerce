from flask import Flask
from mongoengine import connect, disconnect

from backend.conf.settings import Config
from backend.interface.mail import mail
from backend.interface.mongo import mongo, db
from backend.interface.utils import login_manager, bcrypt
from backend.views.main import main
from backend.views.seller import seller
from backend.views.users import users

# from flask_admin import Admin
# from flask_admin.contrib.pymongo import ModelView, filters

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    #admin.add_view(ModelView(User))
    # app.config.from_pyfile('the-config.cfg')
    mongo.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    #connect('mydatabase', host='mongodb://vidulkumar:New2mlab@ds157493.mlab.com:57493/mydatabase')
    connect(db='myDatabase')
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(seller)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)