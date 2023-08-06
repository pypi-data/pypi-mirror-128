import logging
import argparse
import sys

from pyramid.paster import bootstrap, setup_logging

from propfinder import models
from propscraper import get_propscraper

log = logging.getLogger(__name__)


def scrape_properties(dbsession, **kwargs):
    for entry in dbsession.query(models.URL).filter(models.URL.enabled==True):
        dbsession.add(entry)
        kwargs["town"] = entry.location
        log.debug("Scraping properties from {}".format(entry.url))
        scraper = get_propscraper(entry.url)
        for p in scraper:
            dbsession.begin_nested()
            try:
                process_property(dbsession, p, **kwargs)
            except Exception:
                log.exception("Error processing property offer '{}'".format(p.url))
                dbsession.rollback()


def process_property(dbsession, entry, **kwargs):
    entry.process()
    if entry.get_property_type() not in models.Property.property_type.property.columns[0].type.enums:
        log.warn("Skipping property offer '{}'. Unknown property type '{}'.".format(entry.get_id(), entry.get_property_type()))
        return

    offer = dbsession.query(models.PropertyOffer).filter(
        models.PropertyOffer.site==entry.get_site(),
        models.PropertyOffer.offer_id==entry.get_id()
    ).first()
    if offer:
        log.debug("Property offer '{}' already in database".format(entry.get_id()))

        if not offer.active:
            log.debug("Activate property from offer '{}'.".format(entry.get_id()))
            offer.active = True
            offer.property.active = True
            dbsession.add(offer)
            dbsession.add(offer.property)

        price = entry.get_price()
        if price != offer.price:
            offer.price = price
            dbsession.add(offer)
    else:
        town = kwargs["town"]
        dbsession.add(town)

        log.debug("Property offer '{}' not in database".format(entry.get_id()))
        property = models.Property()
        property.location = models.Location.get_from_zone_code(dbsession, entry.get_zone_code(), parent=town)
        property.property_type = entry.get_property_type()
        property.surface = entry.get_surface()
        property.bedrooms = entry.get_bedrooms()
        property.bathrooms = entry.get_bathrooms()
        dbsession.add(property)
        log.debug("Creating property from offer '{}' ".format(entry.get_id()))

        offer = models.PropertyOffer()
        offer.property = property
        offer.site = entry.get_site()
        offer.offer_id = entry.get_id()
        offer.url = entry.url
        offer.price = entry.get_price()
        dbsession.add(offer)
        log.debug("Creating property offer '{}' ".format(entry.get_id()))

    dbsession.flush()


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

    with env['request'].tm:
        dbsession = env['request'].dbsession
        scrape_properties(dbsession)

