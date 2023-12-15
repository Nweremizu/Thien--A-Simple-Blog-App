from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo, URL, Optional
from app.models import User
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 18)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('SIgn In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = CKEditorField('About Me', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        print("Validating username:", username.data)

        if username.data != self.original_username:
            if username.data == "":
                self.username.errors += (ValidationError("Please Enter a Username."),)
                raise ValidationError("Please Enter a Username.")
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                print("Validating username:", username.data)
                self.username.errors += (ValidationError("Please Use a different Username."),)


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    subtitle = StringField('Subtitle', validators=[DataRequired()], render_kw={'placeholder': 'Subtitle'})
    post = CKEditorField('Post', validators=[DataRequired()], render_kw={'placeholder': 'Post'})
    image = FileField('Image', validators=[FileAllowed(['jpg'])])
    image_url = StringField('Image URL', validators=[URL(), Optional()], render_kw={'placeholder': 'Image URL'})
    tags = StringField('Tags', validators=[DataRequired()], render_kw={'placeholder': 'Tags'})

    submit = SubmitField('Publish')


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    subtitle = StringField('Subtitle', validators=[DataRequired()], render_kw={'placeholder': 'Subtitle'})
    post = CKEditorField('Post', validators=[DataRequired()], render_kw={'placeholder': 'Post'})
    image = FileField('Image', validators=[FileAllowed(['jpg'])])
    image_url = StringField('Image URL', validators=[URL(), Optional()], render_kw={'placeholder': 'Image URL'})
    tags = StringField('Tags', validators=[DataRequired()], render_kw={'placeholder': 'Tags'})

    submit = SubmitField('Publish')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
