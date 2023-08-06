import logging
import argparse
import sys

import requests

from pyramid.paster import bootstrap, setup_logging

from propfinder import models

log = logging.getLogger(__name__)

THRESHOLD = 3


class OfferActiveException(Exception):
    pass


def process_active_property_offers(dbsession, **kwargs):
    for offer in dbsession.query(models.PropertyOffer).\
        filter(
            models.PropertyOffer.active==True
        ):

        dbsession.begin_nested()
        dbsession.add(offer)
        offer_id = offer.offer_id
        log.debug("Check property offer {} status".format(offer_id))

        try:
            r = requests.get(offer.url, allow_redirects=False)
            status = models.PropertyOfferStatus()
            status.property_offer_id = offer.id
            status.code = r.status_code
            dbsession.add(status)
            log.debug("Store property offer '{}' with status {}".format(offer_id, status.code))
            kwargs['request'].tm.commit()
        except Exception:
            log.exception("Error processing property offer '#{}'".format(offer_id))
            dbsession.rollback()

def deactivate_property_offers(dbsession, **kwargs):
    for offer in dbsession.query(models.PropertyOffer).filter(models.PropertyOffer.active==True):
        try:
            dbsession.add(offer)
            entries = dbsession.query(models.PropertyOfferStatus.code).\
                filter(
                    models.PropertyOfferStatus.property_offer_id==offer.id
                ).\
                order_by(models.PropertyOfferStatus.created_at.desc()).\
                limit(THRESHOLD).all()

            if len(entries) != THRESHOLD or not all([entry[0] != 200 for entry in entries]):
                raise OfferActiveException()
        except OfferActiveException:
            dbsession.begin_nested()
        else:
            offer.active = False
            dbsession.add(offer)
            log.debug("Property Offer #{} inactive.".format(offer.id))
            kwargs['request'].tm.commit()


def deactivate_properties(dbsession, **kwargs):
    for prop in dbsession.query(models.Property).filter(models.Property.active==True):
        dbsession.add(prop)
        active = any([offer.active for offer in prop.offers])
        if not active:
            prop.active = active
            log.debug("Property #{} inactive.".format(prop.id))
            kwargs['request'].tm.commit()


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    kwargs = {'request': env['request']}

    with env['request'].tm:
        dbsession = env['request'].dbsession
        process_active_property_offers(dbsession, **kwargs)
        deactivate_property_offers(dbsession, **kwargs)
        deactivate_properties(dbsession, **kwargs)

