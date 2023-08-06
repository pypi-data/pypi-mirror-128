#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from chisel.views import EditItemView
from chisel.modeling import cached_getter


class BackOfficeEditView(EditItemView):

    template = 'propfinder:templates/backofficeedit.pt'

    @cached_getter
    def macros_assets(self):
        macros_assets = list(EditItemView.macros_assets)
        macros_assets.append("propfinder:templates/backofficeeditbuttons.pt")
        return macros_assets

