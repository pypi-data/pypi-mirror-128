#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from pyramid.events import NewRequest
from pyramid.i18n import TranslationStringFactory

from chisel.translations import translate

_ = TranslationStringFactory("propfinder")


def setAcceptedLanguagesLocale(event):
    event.request._LOCALE_ = 'en'


def includeme(config):
    config.add_subscriber(setAcceptedLanguagesLocale, NewRequest)

