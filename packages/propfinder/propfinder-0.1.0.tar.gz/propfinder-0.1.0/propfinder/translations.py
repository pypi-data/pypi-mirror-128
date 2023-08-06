#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.feca@gmail.com>
"""
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory("propfinder")


# Translated models
_('vetcrm.models.user.User')
_('vetcrm.models.location.Location')

def includeme(config):
    config.add_translation_dirs(
        'propfinder:locale'
    )

