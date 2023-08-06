#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander
import deform

from pyramid.i18n import TranslationStringFactory

from chisel.schema import ListingFiltersSchema

from propfinder.models import Property
from propfinder.schemas.location import town_selector, zone_selector

_ = TranslationStringFactory("propfinder")


@colander.deferred
def property_type_selector(node, kw):
    values = Property.property_type.property.columns[0].type.enums
    choices = [
        (value, value)
        for value in values
    ]
    choices.insert(0, ('', _("All")))
    return deform.widget.SelectWidget(values=choices)


@colander.deferred
def bedrooms_selector(node, kw):
    return deform.widget.SelectWidget(values=(
        ('', _("All")),
        (1, "+1"),
        (2, "+2"),
        (3, "+3"),
        (4, "+4"),
        (5, "+5"),
    ))


class PropertyListingFiltersSchema(ListingFiltersSchema):

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

    property_type = colander.SchemaNode(
        colander.String(),
        title=_("Type"),
        widget=property_type_selector,
        missing=colander.null
    )

    status = colander.SchemaNode(
        colander.String(),
        title=_("Status"),
        widget=deform.widget.SelectWidget(values=(
            ('active', _("Active")),
            ('inactive', _("Inactive")),
            ('all', _("All")),
        )),
        missing='active'
    )

    bedrooms = colander.SchemaNode(
        colander.Integer(),
        title=_("Bedrooms"),
        widget=bedrooms_selector,
        missing=colander.null
    )

    min_surface = colander.SchemaNode(
        colander.Integer(),
        title=_("Min. surface"),
        missing=colander.null
    )

    max_surface = colander.SchemaNode(
        colander.Integer(),
        title=_("Max. surface"),
        missing=colander.null
    )

    min_price = colander.SchemaNode(
        colander.Integer(),
        title=_("Min. price"),
        missing=colander.null
    )

    max_price = colander.SchemaNode(
        colander.Integer(),
        title=_("Max. price"),
        missing=colander.null
    )

    starred = colander.SchemaNode(
        colander.Boolean(),
        title=_("Starred"),
        missing=colander.null
    )

    elevator = colander.SchemaNode(
        colander.Boolean(),
        title=_("Elevator"),
        missing=colander.null
    )

    parking = colander.SchemaNode(
        colander.Boolean(),
        title=_("Parking"),
        missing=colander.null
    )


class PropertySchema(colander.Schema):

    property_type = colander.SchemaNode(
        colander.String(),
        title=_("Type"),
        widget=property_type_selector
    )

    location_id = colander.SchemaNode(
        colander.Integer(),
        title=_("Location"),
        widget=zone_selector
    )

    address = colander.SchemaNode(
        colander.String(),
        title=_("Address"),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        missing=None
    )

    surface = colander.SchemaNode(
        colander.Integer(),
        title=_("Surface"),
        missing=None
    )

    bedrooms = colander.SchemaNode(
        colander.Integer(),
        title=_("Bedrooms"),
        missing=None
    )

    bathrooms = colander.SchemaNode(
        colander.Integer(),
        title=_("Bathrooms"),
        missing=None
    )

    elevator = colander.SchemaNode(
        colander.Boolean(),
        title=_("Elevator"),
        missing=None
    )

    parking = colander.SchemaNode(
        colander.Boolean(),
        title=_("Parking"),
        missing=None
    )

