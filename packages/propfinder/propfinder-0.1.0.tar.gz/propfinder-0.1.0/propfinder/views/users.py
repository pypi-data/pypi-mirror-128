#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import time

import colander
import deform

import sqlalchemy

from chisel.pkgutils import get_full_name
from chisel.modeling import cached_getter
from chisel.views import (
    Controller,
    FormProcessor,
    Form,
    UsersGrid,
    UsersView as BaseUsersView,
    FiltersForm as BaseFiltersForm,
    EditUserForm as BaseEditUserForm,
    EditUserView as BaseEditUserView,
    DeleteUserView as BaseDeleteUserView
)

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid.i18n import TranslationStringFactory

from chisel.security import has_permission

from propfinder.models import User
from propfinder.schemas.user import (
    UsersListingFiltersSchema,
    UserSchema,
)

_ = TranslationStringFactory("propfinder")


@view_config(route_name='users.listing', permission='view')
class UsersView(BaseUsersView):

    template = 'propfinder:templates/backofficelisting.pt'
    grid_class = UsersGrid
    creation_permission = 'admin'
    edit_permission = 'admin'

    @cached_getter
    def macros_assets(self):
        macros_assets = list(BaseUsersView.macros_assets)
        macros_assets.append(
            "propfinder:templates/backofficelistingbuttons.pt"
        )
        return macros_assets

    class FiltersForm(BaseFiltersForm):

        @cached_getter
        def schema(self):
            return UsersListingFiltersSchema()

    @cached_getter
    def filters_data(self):
        return self.forms['filters_form'].data

    def select_items(self):
        query = BaseUsersView.select_items(self)
        model = self.context.model

        search_query = self.filters_data.get("query", None)
        if search_query:
            query = query.filter(sqlalchemy.or_(
                model.name.like("%%%s%%" % (search_query,)),
                model.email.like("%%%s%%" % (search_query,)),
            ))

        return query


class EditUserForm(BaseEditUserForm):

    @cached_getter
    def schema(self):
        schema = UserSchema()

        if self.controller.is_new:
            del schema["change_password"]

        schema["role"].widget=deform.widget.RadioChoiceWidget(values=(
            ('admin', _('propfinder.models.User.role.admin')),
        ))

        return schema

    def submit(self):
        user = self.controller.item or self.controller.context.model()
        user.name = self.data["name"]
        user.email = self.data["email"]
        user.role = self.data["role"]
        user.enabled = self.data["enabled"]

        if self.data.get("change_password", True):
            user.password = self.data["password"]

        self.dbsession.add(user)
        self.dbsession.flush()
        self.controller.set_item(user)


@view_config(route_name='users.create', permission='edit')
@view_config(route_name='users.create_form', permission='edit')
@view_config(route_name='users.edit', permission='edit')
@view_config(route_name='users.edit_form', permission='edit')
class EditUserView(BaseEditUserView):

    template = 'propfinder:templates/backofficeedit.pt'
    EditUserForm = EditUserForm
    edit_permission = 'admin'

    @cached_getter
    def macros_assets(self):
        macros_assets = list(BaseEditUserView.macros_assets)
        macros_assets.append(
            "propfinder:templates/backofficeeditbuttons.pt"
        )
        return macros_assets


@view_config(route_name='users.delete', permission='admin')
@view_config(route_name='users.delete_form', permission='admin')
class DeleteUserView(BaseDeleteUserView):
    pass


