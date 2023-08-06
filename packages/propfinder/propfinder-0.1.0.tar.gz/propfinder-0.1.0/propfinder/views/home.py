#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jfernandez@bioiberica.com>
"""
import colander
import sqlalchemy
from statistics import mean

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import TranslationStringFactory

from chisel.views import (
    Controller,
    FormProcessor,
    FiltersForm as BaseFiltersForm,
)
from chisel.modeling import cached_getter

from propfinder.models import Location, MonthlyPriceStat
from propfinder.schemas.stats import DashboardFiltersSchema

_ = TranslationStringFactory("propfinder")


@view_config(route_name='home', permission='view')
class HomeView(FormProcessor, Controller):

    template = "propfinder:templates/dashboard.pt"


    class FiltersForm(BaseFiltersForm):

        @cached_getter
        def schema(self):
            return DashboardFiltersSchema()

        @cached_getter
        def bindings(self):
            bindings = BaseFiltersForm.bindings(self)
            bindings["town_selector.empty_option_text"] = _("All")
            bindings["zone_selector.empty_option_text"] = _("All")
            return bindings

    @cached_getter
    def output(self):
        output = Controller.output(self)
        monthly_stats = []
        zone_stats = {}

        data = self.forms["filters_form"].data
        town_id = data.get("town_id", None)
        zone_id = data.get("zone_id", None)

        if town_id:
            if zone_id is not colander.null:
                location_id = zone_id
            else:
                location_id = town_id

            # Monthly stats
            for i in range(12):
                monthly_stats.append(0)

            for month, price in self.request.dbsession.query(MonthlyPriceStat.month, MonthlyPriceStat.price).\
                filter(
                    MonthlyPriceStat.location_id==location_id,
                ):
                monthly_stats[month-1] = str(price)

            # Zone stats
            location = self.request.dbsession.query(Location).filter(Location.id==town_id).one()

            for zone in location.locations:
                zone_stats[zone.location_name] = []
                for i in range(12):
                    zone_stats[zone.location_name].append(0)

            for entry in self.request.dbsession.query(MonthlyPriceStat).\
                join(Location).\
                filter(
                    Location.parent_id==town_id,
                ):
                zone_stats[entry.location.location_name][month-1] = entry.price

        output["monthly_stats"] = monthly_stats
        output["zone_labels"] = list(zone_stats.keys())
        output["zone_stats"] = [str(mean([price for price in prices if price])) for prices in zone_stats.values()]
        return output
