#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander

import sqlalchemy

from pyramid.view import view_config
from pyramid.i18n import TranslationStringFactory

from chisel.modeling import cached_getter
from chisel.views import (
    EditItemForm,
    DeleteItemView,
    DeleteItemForm,
    FiltersForm as BaseFiltersForm,
)
from chisel.itemgrid import CRUDGrid
from chisel.translations import translate

from propfinder.models import URL
from propfinder.schemas.url import (
    URLListingFiltersSchema,
    URLSchema
)
from propfinder.views import BackOfficeListingView, BackOfficeEditView

_ = TranslationStringFactory("propfinder")


class URLsGrid(CRUDGrid):

    @cached_getter
    def schema(self):
        return colander.Schema(
            children=[
                colander.SchemaNode(
                    colander.String(),
                    name='url',
                    title=_("URL")
                ),
                colander.SchemaNode(
                    colander.Boolean(),
                    name='enabled',
                    title=_("Enabled")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='location',
                    title=_("Location")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='description',
                    title=_("Description")
                ),
            ]
        )

    def get_location_value(self, col_num, i, item):
        return item.location.location_name


@view_config(route_name='urls.listing', permission='view')
class URLsController(BackOfficeListingView):

    page_title = _('URLs')
    grid_class = URLsGrid

    class FiltersForm(BaseFiltersForm):

        @cached_getter
        def schema(self):
            return URLListingFiltersSchema()

    @cached_getter
    def filters_data(self):
        return self.forms['filters_form'].data

    def select_items(self):
        query = BackOfficeListingView.select_items(self)
        model = self.context.model

        search_query = self.filters_data.get("query", None)
        if search_query:
            query = query.filter(sqlalchemy.or_(
                model.url.like("%%%s%%" % (search_query,)),
                model.description.like("%%%s%%" % (search_query,)),
            ))

        return query


@view_config(route_name='urls.create', permission='edit')
@view_config(route_name='urls.create_form', permission='edit')
@view_config(route_name='urls.edit', permission='edit')
@view_config(route_name='urls.edit_form', permission='edit')
class EditURLController(BackOfficeEditView):

    class EditURLForm(EditItemForm):

        @cached_getter
        def schema(self):
            return URLSchema()

        def init_data(self, data):
            if not self.controller.is_new:
                item = self.controller.item
                data['url'] = item.url
                data['location_id'] = item.location_id
                data['description'] = item.description
                data['enabled'] = item.enabled

        def submit(self):
            item = self.controller.item or self.controller.context.model()
            item.url = self.data['url']
            item.location_id = self.data['location_id']
            item.description = self.data['description']
            item.enabled = self.data['enabled']

            if self.controller.is_new:
                self.dbsession.add(item)
                self.dbsession.flush()
                self.dbsession.refresh(item)

            self.controller.set_item(item)

    def after_submit(self):
        if self.is_new:
            message = _("New URL created successfully.")
        else:
            message = _("URL updated successfully.")

        self.request.session.flash(translate(message), queue='success')
        BackOfficeEditView.after_submit(self)


@view_config(route_name='urls.delete', permission='edit')
@view_config(route_name='urls.delete_form', permission='edit')
class DeleteURLController(DeleteItemView):

    class DeleteURLForm(DeleteItemForm):

        def after_submit(self):
            self.controller.request.session.flash(
                _("URL deleted successfully."),
                queue='success'
            )
            DeleteItemForm.after_submit(self)

