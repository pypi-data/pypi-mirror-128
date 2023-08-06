#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from webhelpers2.html import tags

import colander

import sqlalchemy

from pyramid.view import view_config
from pyramid.i18n import TranslationStringFactory

from chisel.modeling import cached_getter
from chisel.views import (
    Controller,
    EditItemForm,
    DeleteItemView,
    DeleteItemForm,
    FiltersForm as BaseFiltersForm,
)
from chisel.itemgrid import CRUDGrid
from chisel.translations import translate

from propfinder.models import Location
from propfinder.schemas.location import (
    LocationListingFiltersSchema,
    LocationSchema
)
from propfinder.views import BackOfficeListingView, BackOfficeEditView

_ = TranslationStringFactory("propfinder")


class LocationsGrid(CRUDGrid):

    @cached_getter
    def schema(self):
        return colander.Schema(
            children=[
                colander.SchemaNode(
                    colander.String(),
                    name='code',
                    title=_("Code")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='parent',
                    title=_("Parent")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='location_name',
                    title=_("Name")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='location_type',
                    title=_("Type")
                )
            ]
        )

    def get_parent_value(self, col_num, i, item):
        if item.parent_id:
            return item.parent.location_name

    def get_location_type_value(self, col_num, i, item):
        translation_key = "propfinder.models.location.Location.location_type.%s" % (item.location_type,)
        return translate(_(translation_key))


@view_config(route_name='locations.listing', permission='view')
class LocationsController(BackOfficeListingView):

    page_title = _('Locations')
    grid_class = LocationsGrid

    class FiltersForm(BaseFiltersForm):

        @cached_getter
        def schema(self):
            return LocationListingFiltersSchema()

        @cached_getter
        def bindings(self):
            bindings = BaseFiltersForm.bindings(self)
            bindings["location_type_selector.empty_option_text"] = _("All")
            return bindings

    @cached_getter
    def filters_data(self):
        return self.forms['filters_form'].data

    def select_items(self):
        query = BackOfficeListingView.select_items(self)
        model = self.context.model

        location_type = self.filters_data.get("location_type", None)
        if location_type:
            query = query.filter(
                model.location_type==location_type
            )

        search_query = self.filters_data.get("query", None)
        if search_query:
            query = query.filter(sqlalchemy.or_(
                model.location_name.like("%%%s%%" % (search_query,)),
                model.code==search_query
            ))

        return query


@view_config(route_name='locations.create', permission='edit')
@view_config(route_name='locations.create_form', permission='edit')
@view_config(route_name='locations.edit', permission='edit')
@view_config(route_name='locations.edit_form', permission='edit')
class EditLocationController(BackOfficeEditView):

    class EditLocationForm(EditItemForm):

        @cached_getter
        def schema(self):
            return LocationSchema()

        def init_data(self, data):
            if not self.controller.is_new:
                item = self.controller.item
                data['location_name'] = item.location_name
                data['location_type'] = item.location_type
                data['code'] = item.code
                data['parent_id'] = item.parent_id or colander.null

        def submit(self):
            item = self.controller.item or self.controller.context.model()
            item.location_name = self.data['location_name']
            item.location_type = self.data['location_type']
            item.code = self.data['code']
            item.parent_id = self.data['parent_id']

            if self.controller.is_new:
                self.dbsession.add(item)
                self.dbsession.flush()
                self.dbsession.refresh(item)

            self.controller.set_item(item)

    def after_submit(self):
        if self.is_new:
            message = _("New location created successfully.")
        else:
            message = _("Location updated successfully.")

        self.request.session.flash(translate(message), queue='success')
        BackOfficeEditView.after_submit(self)


@view_config(route_name='locations.delete', permission='edit')
@view_config(route_name='locations.delete_form', permission='edit')
class DeleteLocationController(DeleteItemView):

    class DeleteLocationForm(DeleteItemForm):

        def after_submit(self):
            self.controller.request.session.flash(
                _("Location deleted successfully."),
                queue='success'
            )
            DeleteItemForm.after_submit(self)


@view_config(route_name='locations.values', permission='view')
class LocationValuesController(Controller):

    default_rendering_format = "json"
    allowed_rendering_formats = ("json",)

    @cached_getter
    def output(self):
        values = {}
        for location in self.context.item.locations:
            values[location.id] = location.location_name

        return values

