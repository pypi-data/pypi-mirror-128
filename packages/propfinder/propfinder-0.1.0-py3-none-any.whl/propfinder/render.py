#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from pyramid.events import BeforeRender

from chisel.templates import TemplateAPI


def add_renderer_globals(event):
    request = event['request']
    api = getattr(request, 'template_api', None)
    if api is None and request is not None:
        api = TemplateAPI(event['context'], event['request'])
    event['api'] = api


def includeme(config):
    config.add_subscriber(
        add_renderer_globals,
        BeforeRender
    )

