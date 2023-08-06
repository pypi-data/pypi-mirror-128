#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander
import deform

from sqlalchemy.orm import aliased

from pyramid.i18n import TranslationStringFactory

from propfinder.models import Location

_ = TranslationStringFactory("propfinder")


@colander.deferred
def location_type_selector(node, kw):
    empty_option = node.bindings.get("location_type_selector.empty_option", True)
    empty_option_text = node.bindings.get("location_type_selector.empty_option_text", "")

    choices = [
        ("continent", _("propfinder.models.location.Location.location_type.continent")),
        ("country", _("propfinder.models.location.Location.location_type.country")),
        ("autonomous_community", _("propfinder.models.location.Location.location_type.autonomous_community")),
        ("province", _("propfinder.models.location.Location.location_type.province")),
        ("town", _("propfinder.models.location.Location.location_type.town")),
        ("zone", _("propfinder.models.location.Location.location_type.zone"))
    ]

    if empty_option:
        choices.insert(0, ("", empty_option_text))

    return deform.widget.SelectWidget(values=choices)


class LocationListingFiltersSchema(colander.Schema):

    location_type = colander.SchemaNode(
        colander.String(),
        title=_("Type"),
        widget=location_type_selector,
        missing=colander.null
    )

    query = colander.SchemaNode(
        colander.String(),
        title=_("Search"),
        missing=colander.null
    )


class LocationSchema(colander.Schema):

    location_name = colander.SchemaNode(
        colander.String(),
        title=_("Name")
    )

    location_type = colander.SchemaNode(
        colander.String(),
        title=_("Type"),
        widget=location_type_selector
    )

    code = colander.SchemaNode(
        colander.String(),
        title=_("Code"),
        widget=deform.widget.TextAreaWidget(rows=10, cols=60)
    )

    parent_id = colander.SchemaNode(
        colander.Integer(),
        title=_("Parent"),
        missing=None
    )


@colander.deferred
def province_selector(node, kw):
    request = kw["request"]
    country = node.bindings.get("country", "ES")
    autonomous_community = node.bindings.get("autonomous_community", None)

    Country = aliased(Location)
    AutonomusCommunity = aliased(Location)

    query = request.dbsession.query(Location).\
        join(AutonomusCommunity, AutonomusCommunity.id==Location.parent_id).\
        join(Country, Country.id==AutonomusCommunity.parent_id).filter(
            Location.location_type == "province",
            AutonomusCommunity.location_type == "autonomous_community",
            Country.location_type == "country",
            Country.code == country
        ).\
        order_by(Location.location_name)

    if autonomous_community:
        query = query.filter(
            AutonomusCommunity.code == autonomous_community
        )

    choices = [
        (entry.id, entry.location_name)
        for entry in query
    ]

    choices.insert(0, ('', _("All")))
    return deform.widget.Select2Widget(values=choices)


@colander.deferred
def town_selector(node, kw):
    request = kw["request"]
    Province = aliased(Location)
    empty_option = node.bindings.get("town_selector.empty_option", True)
    empty_option_text = node.bindings.get("town_selector.empty_option_text", "")

    query = request.dbsession.query(Location).\
        join(Province, Province.id==Location.parent_id).filter(
            Location.location_type == "town",
            Province.location_type == "province",
        ).\
        order_by(Location.location_name)

    province_id = node.bindings.get('town_selector.province_id', None)
    if province_id:
        query = query.filter(
            Province.id == province_id
        )

    choices = [
        (entry.id, entry.location_name)
        for entry in query
    ]

    if empty_option:
        choices.insert(0, ('', empty_option_text))

    return deform.widget.Select2Widget(values=choices)


@colander.deferred
def zone_selector(node, kw):
    request = kw["request"]
    Town = aliased(Location)
    empty_option = node.bindings.get("zone_selector.empty_option", True)
    empty_option_text = node.bindings.get("zone_selector.empty_option_text", "")
    multiple = node.bindings.get("zone_selector.multiple", False)

    query = request.dbsession.query(Location).\
        join(Town, Town.id==Location.parent_id).filter(
            Location.location_type == "zone",
            Town.location_type == "town",
        ).\
        order_by(Location.location_name)

    town_id = node.bindings.get('zone_selector.town_id', None)
    if town_id:
        query = query.filter(
            Town.id == town_id
        )

    choices = [
        (entry.id, entry.location_name)
        for entry in query
    ]

    if empty_option:
        choices.insert(0, ('', empty_option_text))

    return deform.widget.Select2Widget(values=choices, multiple=multiple)

