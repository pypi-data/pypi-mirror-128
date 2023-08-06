#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    Unicode,
    UnicodeText,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from .meta import Base
from . import ItemMixin


class URL(ItemMixin, Base):
    __tablename__ = 'urls'

    url = Column(Unicode(255), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    location = relationship(
        "propfinder.models.location.Location",
        lazy='joined'
    )
    description = Column(UnicodeText())
    enabled = Column(Boolean(name='ck_url_enabled'), default=True, index=True)

