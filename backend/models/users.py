from bson.objectid import ObjectId
from flask import current_app
from flask_admin.contrib.pymongo import ModelView
from flask_login import UserMixin
from flask_login import current_user
from flask_wtf import FlaskForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, \
    IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from backend.interface.mongo import db, mongo
from backend.interface.utils import login_manager

#from flask_admin.contrib.mongoengine import ModelView


class User(UserMixin, db.Document):
    #meta = {'collection': 'users'}
    #meta = {'DB': 'myDatabase'}
    username = db.StringField(max_length=30)
    email = db.EmailField(max_length=30)
    password = db.StringField()
    role = db.StringField()
    approved = db.BooleanField()
    isactive = db.BooleanField()
    item = db.StringField()
    wishlist = db.StringField()
    list_address = db.StringField()

    def __rep__(self):
        return 'User({},{})'.format(self.username, self.email)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        print('Serializer working',type(self.id))
        #print(ObjectId(self.get_id).valueOf())
        print('noooooooooooooooooo',self.id,'       ',self.get_id())
        return s.dumps({'user_id': str(self.get_id())}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        print(type(user_id))
        print('yesssssssssssssssssssssssssssss   ',user_id)
        return User.objects(pk=ObjectId(user_id)).first()

# with switch_db(User, 'archive') as User:
# User(name='Ross').save()  # Saves the 'archive-user-db'
'''
hashpass = generate_password_hash("mohitarora123", method='sha256')
role = 'admin'
User("Mohit Arora","arora3mohit@gmail.com",hashpass,role).save()
'''
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class UserView(ModelView):
    column_list = ('name', 'email', 'password')
    column_sortable_list = ('name', 'email', 'password')

    form = User

'''
class UserView(ModelView):
    column_list = ('name', 'email', 'password')
    column_sortable_list = ('name', 'email', 'password')
    form = User


aadmin.add_view(ModelView(User))

'''
#admin.add_view(ModelView(Post, db.session))
# Admin.add_view(UserView(User))





class ReviewForm(FlaskForm):
    rating = IntegerField('Overall Rating', validators=[DataRequired()])

    def validate_rating(self, rating):
        if rating.data < 1 or rating.data > 5:
            raise ValidationError('Rating should be in between 1 and 5')
    headline = StringField('Add a headline', validators=[DataRequired()])
    review = TextAreaField('Write your review')
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    seller = BooleanField('Register as Seller')

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        users = mongo.db.user
        user = users.find_one({'username': username.data})
        if user:
            raise ValidationError('That username is alreay taken. Please choose a different one')

    def validate_email(self, email):
        users = mongo.db.user
        user = users.find_one({'email': email.data})
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DeliveryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=15)])
    address = TextAreaField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pin_code = IntegerField('Pin Code', validators=[DataRequired()])
    phone_number = StringField('Mobile Number', validators=[DataRequired(), Length(10)])
    submit = SubmitField('Save')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        users = mongo.db.user
        print(email.data)
        user = users.find_one({'email': email.data})
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateAccountForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is alreay taken. Please choose a different one.')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('This email is alreay taken. Please choose a different one.')

