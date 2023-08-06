import argparse
import sys
from getpass import getpass

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from propfinder import models
from propfinder.propertyfinder import get_property_finder


def setup_models(dbsession, **kwargs):
    """
    Add or update models / fixtures in the database.

    """
    if kwargs.get("setup_admin", False):
        setup_admin(dbsession, **kwargs)

    if kwargs.get("update_locations", False):
        update_locations(dbsession, **kwargs)


def setup_admin(dbsession, **kwargs):
    print("Creating the admin user")
    admin = models.User()
    admin.name = "Jordi Fernández"
    admin.email = "jordi.feca@gmail.com"
    admin.role = "admin"
    admin.enabled = True
    admin.password = getpass()
    dbsession.add(admin)

def update_locations(dbsession, **kwargs):
    barcelona = dbsession.query(models.Location).filter(
        models.Location.location_type=="province",
        models.Location.code=="08"
    ).first()

    if not barcelona:
        barcelona = models.Location()
        barcelona.location_name = "Barcelona"
        barcelona.location_type = "province"
        barcelona.code = "08"
        dbsession.add(barcelona)

    tordera = dbsession.query(models.Location).filter(
        models.Location.location_type=="town",
        models.Location.code=="2845"
    ).first()

    if not tordera:
        tordera = models.Location()
        tordera.parent = barcelona
        tordera.location_name = "Tordera"
        tordera.location_type = "town"
        tordera.code = "2845"
        dbsession.add(tordera)

    girona = dbsession.query(models.Location).filter(
        models.Location.location_type=="province",
        models.Location.code=="17"
    ).first()

    if not girona:
        girona = models.Location()
        girona.location_name = "Girona"
        girona.location_type = "province"
        girona.code = "17"
        dbsession.add(girona)

    blanes = dbsession.query(models.Location).filter(
        models.Location.location_type=="town",
        models.Location.code=="0237"
    ).first()

    if not blanes:
        blanes = models.Location()
        blanes.parent = girona
        blanes.location_name = "Blanes"
        blanes.location_type = "town"
        blanes.code = "0237"
        dbsession.add(blanes)

    for entry in dbsession.query(models.URL).filter(models.URL.enabled==True):
        zones = {}
        f = get_property_finder(entry.url)
        for p in f:
            p.process()
            code = p.get_zone_code()
            if code:
                zone = zones.get(code, None)
                if zone is None:
                    zone = models.Location()
                    zone.parent = entry.location
                    zone.location_name = code
                    zone.location_type = "zone"
                    zone.code = code
                    dbsession.add(zone)
                    dbsession.flush()
                    zones[code] = zone


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    parser.add_argument(
        '--setup_admin',
        dest='setup_admin',
        action='store_true',
        help='Setup the admin user',
    )
    parser.add_argument(
        '--update_locations',
        dest='update_locations',
        action='store_true',
        help='Update the locations database',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    kwargs = {
        'setup_admin': args.setup_admin,
        'update_locations': args.update_locations
    }

    with env['request'].tm:
        dbsession = env['request'].dbsession
        setup_models(dbsession, **kwargs)

