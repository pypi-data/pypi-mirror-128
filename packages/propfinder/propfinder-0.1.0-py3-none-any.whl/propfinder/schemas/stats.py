#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander
import deform

from pyramid.i18n import TranslationStringFactory

from propfinder.schemas.location import town_selector, zone_selector

_ = TranslationStringFactory("propfinder")


class DashboardFiltersSchema(colander.Schema):

    town_id = colander.SchemaNode(
        colander.Integer(),
        title=_("Town"),
        widget=town_selector,
        missing=colander.null
    )

    zone_id = colander.SchemaNode(
        colander.Integer(),
        title=_("Zone"),
        widget=zone_selector,
        missing=colander.null
    )

