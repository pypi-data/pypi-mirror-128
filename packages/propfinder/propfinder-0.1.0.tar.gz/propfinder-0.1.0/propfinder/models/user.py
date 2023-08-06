#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from hashlib import sha512

from sqlalchemy import (
    Column,
    Unicode,
    String,
    Boolean
)
from sqlalchemy.orm import synonym

from pyramid.i18n import TranslationStringFactory

from .meta import Base
from . import ItemMixin

_ = TranslationStringFactory("vetcrm")


class User(ItemMixin, Base):
    __tablename__ = 'users'
    name = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    role = Column(Unicode(255), nullable=False)
    enabled = Column(Boolean(name='ck_user_enabled'), default=True)
    password_ = Column('password', String(128)) # Hash from sha512
    encryption_method = sha512

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, password):
        self.password_ = self.encryption(password)

    password = synonym('password_', descriptor=password)

    @classmethod
    def encryption(cls, data):
        if cls.encryption_method:
            if isinstance(data, str):
                data = data.encode('utf-8')

            data = cls.encryption_method(data).hexdigest()

        return data

    def validate_password(self, password):
        return self.password == self.encryption(password)

