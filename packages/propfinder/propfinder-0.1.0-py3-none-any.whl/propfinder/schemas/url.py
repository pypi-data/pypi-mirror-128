#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander
import deform

from pyramid.i18n import TranslationStringFactory

from propfinder.schemas.location import town_selector

_ = TranslationStringFactory("propfinder")


class URLListingFiltersSchema(colander.Schema):

    query = colander.SchemaNode(
        colander.String(),
        title=_("Search"),
        missing=colander.null
    )


class URLSchema(colander.Schema):

    url = colander.SchemaNode(
        colander.String(),
        title=_("URL")
    )

    enabled = colander.SchemaNode(
        colander.Boolean(),
        title=_("Enabled"),
        default=True
    )

    location_id = colander.SchemaNode(
        colander.Integer(),
        title=_("Location"),
        widget=town_selector
    )

    description = colander.SchemaNode(
        colander.String(),
        title=_("Description"),
        widget=deform.widget.TextAreaWidget(rows=10, cols=60)
    )

