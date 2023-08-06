#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander
from webhelpers2.html import HTML, tags

import sqlalchemy

from pyramid.view import view_config
from pyramid.i18n import TranslationStringFactory
from pyramid.renderers import render

from chisel.modeling import cached_getter
from chisel.views import (
    Controller,
    EditItemForm,
    DeleteItemView,
    DeleteItemForm,
    AjaxFormController,
    AjaxForm,
    FiltersForm as BaseFiltersForm,
)
from chisel.itemgrid import ItemGrid, CRUDGrid
from chisel.translations import translate

from propfinder.models import (
    Property,
    PropertyOffer,
    PropertyOfferPriceChange,
    Location
)
from propfinder.schemas.property import (
    PropertyListingFiltersSchema,
    PropertySchema
)
from propfinder.views import BackOfficeListingView, BackOfficeEditView

_ = TranslationStringFactory("propfinder")


class PropertiesGrid(CRUDGrid):

    delete_permission = "delete"

    @cached_getter
    def schema(self):
        return colander.Schema(
            children=[
                colander.SchemaNode(
                    colander.String(),
                    name='flags',
                    title=_("")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='id',
                    title=_("#ID")
                ),
                colander.SchemaNode(
                    colander.DateTime(),
                    name='created_at',
                    title=_("Creation Time")
                ),
                colander.SchemaNode(
                    colander.DateTime(),
                    name='updated_at',
                    title=_("Last update")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='property_type',
                    title=_("Type")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='location_id',
                    title=_("Location")
                ),
                colander.SchemaNode(
                    colander.Decimal(quant='0.01'),
                    name='surface',
                    title=_("Surface")
                ),
                colander.SchemaNode(
                    colander.Integer(),
                    name='price',
                    title=_("Price")
                ),
                colander.SchemaNode(
                    colander.Integer(),
                    name='price_m2',
                    title=_("Price m2")
                ),
                colander.SchemaNode(
                    colander.Integer(),
                    name='bedrooms',
                    title=_("Bedrooms")
                ),
                colander.SchemaNode(
                    colander.Integer(),
                    name='bathrooms',
                    title=_("Bathrooms")
                ),
                colander.SchemaNode(
                    colander.Boolean(),
                    name='elevator',
                    title=_("Elevator")
                ),
                colander.SchemaNode(
                    colander.Boolean(),
                    name='parking',
                    title=_("Parking")
                ),
            ]
        )

    def get_record_css_class(self, i, record, columns):
        class_name = CRUDGrid.get_record_css_class(self, i, record, columns)
        if not record.active:
            class_name = "%s inactive" % (class_name,)
        return class_name

    def get_flags_value(self, col_num, i, item):
        css = ["toggle-starred", "fa-star"]
        if item.starred:
            css.append("fa")
        else:
            css.append("far")

        return tags.Link(
            u" ",
            url="#",
            data_toggle_starred=self.request.route_url(
                "properties.toggle_starred",
                id=item.id
            ),
            class_=" ".join(css),
        )

    def get_location_id_value(self, col_num, i, item):
        return "%s > %s" % (item.location.parent.location_name, item.location.location_name)

    def get_price_m2_value(self, col_num, i, item):
        if item.surface:
            return int(item.price / item.surface)

    def get_actions_links(self, col_num, i, item):
        links = CRUDGrid.get_actions_links(self, col_num, i, item)

        # Price changes
        links.append(
            tags.Link(
                u" ",
                url=self.request.route_url(
                    'properties.price_changes',
                    id=item.id
                ),
                data_toggle="modal",
                data_target="#dynamic-modal",
                class_="fa fa-chart-line",
                title=translate(_("Price changes")),
            )
        )

        # Open offer link
        button = render(
            'propfinder:templates/openofferlink.pt',
            {'item': item, 'offers': [offer for offer in item.offers if offer.active]},
            request=self.request
        )
        links.append(HTML.literal(button))

        # Join
        links.append(
            tags.Link(
                u" ",
                url=self.request.route_url(
                    "properties.join",
                    id=item.id,
                ),
                data_toggle="modal",
                data_target="#dynamic-modal",
                class_="far fa-share-square",
                title=translate(_("Join offer")),
            )
        )

        return links


@view_config(route_name='properties.listing', permission='view')
class PropertiesController(BackOfficeListingView):

    page_title = _('Properties')
    grid_class = PropertiesGrid
    default_order = "-updated_at"
    allow_ordering = ["created_at", "updated_at", "property_type", "surface", "price", "price_m2", "bedrooms", "bathrooms", "location_id"]
    allow_grouping = ["property_type", "surface", "price", "price_m2", "bedrooms", "bathrooms", "location_id"]
    template = "propfinder:templates/propertieslisting.pt"

    class FiltersForm(BaseFiltersForm):

        @cached_getter
        def schema(self):
            return PropertyListingFiltersSchema()

        @cached_getter
        def bindings(self):
            bindings = BaseFiltersForm.bindings(self)
            bindings["town_selector.empty_option_text"] = _("All")
            bindings["zone_selector.empty_option_text"] = _("All")
            return bindings

    @cached_getter
    def filters_data(self):
        return self.forms['filters_form'].data

    def select_items(self):
        query = BackOfficeListingView.select_items(self).join(Location)
        model = self.context.model

        town_id = self.filters_data.get("town_id", None)
        if town_id:
            query = query.filter(
                Location.parent_id==town_id
            )

        zone_id = self.filters_data.get("zone_id", None)
        if zone_id:
            query = query.filter(
                model.location_id==zone_id
            )

        min_surface = self.filters_data.get("min_surface", None)
        if min_surface:
            query = query.filter(
                model.surface>=min_surface
            )

        max_surface = self.filters_data.get("max_surface", None)
        if max_surface:
            query = query.filter(
                model.surface<=max_surface
            )

        min_price = self.filters_data.get("min_price", None)
        if min_price:
            query = query.filter(
                model.price>=min_price
            )

        max_price = self.filters_data.get("max_price", None)
        if max_price:
            query = query.filter(
                model.price<=max_price
            )

        status = self.filters_data.get("status", 'active')
        if status == 'all':
            pass
        elif status == 'inactive':
            query = query.filter(
                model.active==False
            )
        else:
            query = query.filter(
                model.active==True
            )

        starred = self.filters_data.get("starred", False)
        if starred:
            query = query.filter(
                model.starred==True
            )

        bedrooms = self.filters_data.get("bedrooms", None)
        if bedrooms:
            query = query.filter(
                model.bedrooms>=bedrooms
            )

        elevator = self.filters_data.get("elevator", False)
        if elevator:
            query = query.filter(
                model.elevator==True
            )

        parking = self.filters_data.get("parking", False)
        if parking:
            query = query.filter(
                model.parking==True
            )

        property_type = self.filters_data.get("property_type", None)
        if property_type:
            query = query.filter(
                model.property_type==property_type
            )

        return query

    def order_by_price_m2(self, query, sign):
        return query.order_by(sign(Property.price/Property.surface))


@view_config(route_name='properties.edit', permission='edit')
@view_config(route_name='properties.edit_form', permission='edit')
class EditPropertyController(BackOfficeEditView):

    class EditPropertyForm(EditItemForm):

        @cached_getter
        def schema(self):
            return PropertySchema()

        def init_data(self, data):
            if not self.controller.is_new:
                item = self.controller.item
                data['property_type'] = item.property_type
                data['location_id'] = item.location_id
                data['address'] = item.address or colander.null
                data['surface'] = item.surface or colander.null
                data['bedrooms'] = item.bedrooms or colander.null
                data['bathrooms'] = item.bathrooms or colander.null
                data['elevator'] = item.elevator or colander.null
                data['parking'] = item.parking or colander.null

        def submit(self):
            item = self.controller.item or self.controller.context.model()
            item.property_type = self.data['property_type']
            item.location_id = self.data['location_id']
            item.address = self.data['address'] or None
            item.surface = self.data['surface'] or None
            item.bedrooms = self.data['bedrooms'] or None
            item.bathrooms = self.data['bathrooms'] or None
            item.elevator = self.data['elevator']
            item.parking = self.data['parking']

    def after_submit(self):
        message = _("Property updated successfully.")
        self.request.session.flash(translate(message), queue='success')
        BackOfficeEditView.after_submit(self)


class PriceChangesGrid(ItemGrid):

    @cached_getter
    def schema(self):
        return colander.Schema(
            children=[
                colander.SchemaNode(
                    colander.DateTime(),
                    name='created_at',
                    title=_("Date")
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='site',
                    title=_("Site"),
                ),
                colander.SchemaNode(
                    colander.String(),
                    name='offer_id',
                    title=_("Offer ID"),
                ),
                colander.SchemaNode(
                    colander.Integer(),
                    name='price',
                    title=_("Price"),
                ),
            ]
        )

    def get_site_value(self, col_num, i, item):
        return item.property_offer.site

    def get_offer_id_value(self, col_num, i, item):
        return item.property_offer.offer_id


@view_config(route_name='properties.price_changes', permission='view')
class PriceChangesController(Controller):

    template = 'propfinder:templates/pricechanges.pt'

    @cached_getter
    def output(self):
        output = Controller.output(self)
        output["title"] = "Price changes"
        output["content"] = PriceChangesGrid(self.context.item.price_changes)
        return output


@view_config(route_name='properties.toggle_starred', permission='edit')
class ToggleStarredController(Controller):

    default_rendering_format = "json"
    allowed_rendering_formats = ("json",)

    def submit(self):
        self.context.item.starred = not self.context.item.starred

    @cached_getter
    def output(self):
        return {'starred': self.context.item.starred}


@view_config(route_name='properties.join', permission='edit')
class JoinProperties(AjaxFormController):

    @cached_getter
    def item_id(self):
        return self.context.item_id

    @cached_getter
    def item(self):
        return self.context.item

    @cached_getter
    def return_url(self):
        return self.request.route_url('properties.listing')

    class JoinPropertiesForm(AjaxForm):

        submit_button_title = _("Join")

        @cached_getter
        def action_url(self):
            return self.controller.request.route_url(
                'properties.join',
                id=self.controller.item_id
            )

        @cached_getter
        def schema(self):
            schema = colander.Schema(
                title=translate(_("Join property to")),
                description=HTML.literal(
                    """<div class="alert-info property-info">
                        <h3>#%s - %s %s</h3>
                        <p><strong>%s:</strong> %s m<sup>2</sup></p>
                        <p><strong>%s:</strong> %s €</p>
                    </div>
                    """ % (
                        self.controller.item.id,
                        self.controller.item.location.parent.location_name,
                        self.controller.item.location.location_name,
                        translate(_("Surface")),
                        self.controller.item.surface,
                        translate(_("Price")),
                        self.controller.item.price,
                    )
                ),
                children=[
                    colander.SchemaNode(
                        colander.Integer(),
                        name="property_id",
                        title=_("Destination property")
                    )
                ]
            )
            return schema

        def submit(self):
            property = self.dbsession.query(Property).get(self.data["property_id"])
            for offer in list(self.controller.item.offers):
                offer.property = property
                self.dbsession.add(offer)
            self.dbsession.flush()
            self.dbsession.delete(self.controller.item)

        def after_submit(self):
            message = _("Property successfully joined.")
            self.controller.request.session.flash(translate(message), queue='success')

