#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
import colander
import deform

from sqlalchemy.orm.exc import NoResultFound

from pyramid.view import (
    view_config,
    forbidden_view_config,
)
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.i18n import TranslationStringFactory

from chisel.modeling import cached_getter
from chisel.views import FormProcessor, Form, AuthView

from propfinder.models import User

_ = TranslationStringFactory("propfinder")


class LoginSchema(colander.Schema):

    username = colander.SchemaNode(
        colander.String(),
        title=_("Username")
    )

    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.PasswordWidget(),
        title=_("Password")
    )

    came_from = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        missing=None
    )


@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED)
class PropFinderAuthView(FormProcessor, AuthView):

    template = 'propfinder:templates/login.pt'

    class LoginForm(Form):

        schema = LoginSchema()
        actions = ('login',)
        user = None
        login_succeed = False

        def create_form(self, **kwargs):
            kwargs.update(
                action=self.controller.request.route_url('login'),
                buttons=(
                    deform.Button(
                        title=_("Login"),
                        value="login",
                        css_class="btn btn-primary"
                    ),
                ),
                autocomplete=False,
                bootstrap_form_style='form-vertical'
            )
            return Form.create_form(self, **kwargs)

        def init_data(self, data):
            data.update(came_from=self.controller.came_from)

        def submit(self):
            username = self.data.get('username')
            password = self.data.get('password')

            try:
                self.user = self.controller.request.dbsession.query(User)\
                    .filter(User.email==username)\
                    .filter(User.enabled==True)\
                    .one()
            except NoResultFound:
                pass

            if not self.user or not password or not self.user.validate_password(password.encode('utf-8')):
                return

            self.login_succeed = True

        def after_submit(self):
            if self.login_succeed:
                self.controller.login(self.user.id)

        def render(self):
            return self.form.render()


    @cached_getter
    def output(self):
        output = AuthView.output(self)
        login_form = self.forms["login_form"]
        output['login_failed'] = self.submitted and self.valid and not login_form.login_succeed
        return output

    @view_config(route_name='logout', permission=NO_PERMISSION_REQUIRED)
    def logout(self):
        return AuthView.logout(self)

    @forbidden_view_config(renderer='propfinder:templates/forbidden.pt')
    def forbidden_view(self):
        return AuthView.forbidden_view(self)

