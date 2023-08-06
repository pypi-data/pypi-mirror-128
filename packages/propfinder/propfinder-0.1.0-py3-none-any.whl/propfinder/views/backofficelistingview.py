#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from chisel.views import ListingView
from chisel.modeling import cached_getter


class BackOfficeListingView(ListingView):

    creation_permission = 'create'
    edit_permission = 'edit'
    template = 'propfinder:templates/backofficelisting.pt'

    @cached_getter
    def macros_assets(self):
        macros_assets = list(ListingView.macros_assets)
        macros_assets.append("propfinder:templates/backofficelistingbuttons.pt")
        return macros_assets

