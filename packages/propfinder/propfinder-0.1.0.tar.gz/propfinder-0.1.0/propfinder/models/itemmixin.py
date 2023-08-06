#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    event
)
from sqlalchemy.sql import text

from pyramid.i18n import TranslationStringFactory

from chisel.pkgutils import get_full_name
from chisel.translations import translate

from .meta import Base

_ = TranslationStringFactory("propfinder")


class ItemMixin(object):

    __versioned__ = {}

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def update_updated_at(mapper, connection, target):
        target.updated_at = datetime.now()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_update', cls.update_updated_at)

    def get_representative_id(self):
        return "#%s" % (self.id,)

    def __str__(self):
        return "%s %s" % (
            translate(_(get_full_name(self.__class__))),
            self.get_representative_id()
        )

