#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander

from pyramid.i18n import TranslationStringFactory

from chisel.schema.user import UserSchema

_ = TranslationStringFactory("propfinder")


class UsersListingFiltersSchema(colander.Schema):

    query = colander.SchemaNode(
        colander.String(),
        title=_("Search"),
        missing=colander.null
    )

