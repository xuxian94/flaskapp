# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User


class RegisterForm(Form):
    """Register form."""
    LANGUAGES = ['zh']

    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('密码',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('确认密码',
                            [DataRequired(), EqualTo('password', message='两次密码必须相同')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('用户名已注册！')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('邮箱已注册！')
            return False
        return True
