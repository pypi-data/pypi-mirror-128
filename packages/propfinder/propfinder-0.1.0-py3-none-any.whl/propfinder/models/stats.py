#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from statistics import mean
from datetime import date

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Date,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship, backref

from pyramid.threadlocal import get_current_request

from .meta import Base
from . import Property


class DailyPriceStat(Base):
    __tablename__ = 'daily_price_stats'

    day = Column(Date, nullable=False, primary_key=True, default=date.today)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    location = relationship(
        "propfinder.models.location.Location",
        lazy='joined'
    )
    price = Column(Numeric(7, 2), nullable=False)

    @classmethod
    def update(cls):
        request = get_current_request()
        stats = {}

        # Delete previous stats
        request.dbsession.execute(
            cls.__table__.delete().where(cls.__table__.c.day==date.today())
        )

        for prop in request.dbsession.query(Property).filter(Property.active==True):
            if prop.surface and prop.price:
                price = prop.price/prop.surface
                zone_prices = stats.setdefault(prop.location_id, [])
                zone_prices.append(price)
                town_prices = stats.setdefault(prop.location.parent_id, [])
                town_prices.append(price)

        for location_id, prices in stats.items():
            stat = cls()
            stat.location_id = location_id
            stat.price = mean(prices)
            request.dbsession.add(stat)


class MonthlyPriceStat(Base):
    __tablename__ = 'monthly_price_stats'

    month = Column(Integer, nullable=False, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    location = relationship(
        "propfinder.models.location.Location",
        lazy='joined'
    )
    price = Column(Numeric(7, 2), nullable=False)

    @classmethod
    def update(cls):
        request = get_current_request()
        month = date.today().month
        stats = {}

        # Delete previous stats
        request.dbsession.execute(
            cls.__table__.delete().where(cls.__table__.c.month==month)
        )

        for stat in request.dbsession.query(DailyPriceStat).filter(func.extract('month', DailyPriceStat.day)==month):
            prices = stats.setdefault(stat.location_id, [])
            prices.append(stat.price)

        for location_id, prices in stats.items():
            stat = cls()
            stat.month = month
            stat.location_id = location_id
            stat.price = mean(prices)
            request.dbsession.add(stat)

