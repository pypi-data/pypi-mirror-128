#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    Unicode,
    UnicodeText,
    Enum,
    ForeignKey,
    event,
    func
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import select

from pyramid.threadlocal import get_current_request

from chisel.modeling import cached_getter

from .meta import Base
from . import ItemMixin


class Property(ItemMixin, Base):
    __tablename__ = 'properties'

    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    location = relationship(
        "propfinder.models.location.Location",
        lazy='joined',
        backref=backref("properties")
    )
    address = Column(UnicodeText)

    property_type = Column(
        Enum(
            "house",
            "flat",
            "duplex",
            "penthouse",
            "ground_floor",
        ),
        index=True
    )

    price = Column(Integer, index=True)

    surface = Column(Integer, index=True)

    bedrooms = Column(Integer, index=True)
    bathrooms = Column(Integer, index=True)
    elevator = Column(Boolean(name='ck_property_elevator'), index=True)
    parking = Column(Boolean(name='ck_property_parking'), index=True)

    starred = Column(Boolean(name='ck_property_starred'), index=True, default=False)
    active = Column(Boolean(name='ck_property_active'), index=True, default=True)

    @cached_getter
    def price_changes(self):
        request = get_current_request()
        return request.dbsession.query(PropertyOfferPriceChange).\
            join(PropertyOffer).\
            filter(PropertyOffer.property_id==self.id).\
            order_by(PropertyOfferPriceChange.created_at.desc()).all()


class PropertyOffer(ItemMixin, Base):
    __tablename__ = 'property_offers'

    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    property = relationship(
        "propfinder.models.property.Property",
        lazy='joined',
        backref=backref("offers")
    )

    site = Column(Unicode(50), nullable=False, index=True)
    offer_id = Column(Unicode(50), nullable=False, index=True)
    url = Column(Unicode(255), nullable=False)
    price = Column(Integer, nullable=False, index=True)

    active = Column(Boolean(name='ck_property_offer_active'), index=True, default=True)

    @staticmethod
    def update_property_price(mapper, connection, target):
        offers = target.__table__
        table = target.property.__table__

        # Update the minimum price of the property
        stmt = table.update().where(table.c.id==target.property_id).\
            values(
                updated_at=datetime.now(),
                price=select([func.min(offers.c.price)]).where(
                    offers.c.property_id==target.property_id
                )
            )
        connection.execute(stmt)

        # Register the price change
        stmt = PropertyOfferPriceChange.__table__.insert().values(
            created_at=datetime.now(),
            property_offer_id=target.id,
            price=target.price
        )
        connection.execute(stmt)

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'after_insert', cls.update_property_price)
        event.listen(cls, 'after_update', cls.update_property_price)


class PropertyOfferPriceChange(Base):
    __tablename__ = 'property_offer_price_changes'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)

    property_offer_id = Column(Integer, ForeignKey('property_offers.id', name="fk_prop_offer_price_changes__prop_offer"), nullable=False)
    property_offer = relationship(
        "propfinder.models.property.PropertyOffer",
        lazy='joined',
        backref=backref("price_changes")
    )

    price = Column(Integer, nullable=False)


class PropertyOfferStatus(Base):
    __tablename__ = 'property_offer_status'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)

    property_offer_id = Column(Integer, ForeignKey('property_offers.id', name="fk_prop_offer_status__prop_offer"), nullable=False)
    property_offer = relationship(
        "propfinder.models.property.PropertyOffer",
        lazy='joined',
        backref=backref("status")
    )

    code = Column(Integer, nullable=False)

