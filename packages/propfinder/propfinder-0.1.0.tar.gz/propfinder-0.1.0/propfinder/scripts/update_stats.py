import logging
import argparse
import sys

from pyramid.paster import bootstrap, setup_logging

from propfinder import models

log = logging.getLogger(__name__)


def update_stats(dbsession, **kwargs):
    models.DailyPriceStat.update()
    models.MonthlyPriceStat.update()


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
        update_stats(dbsession, **kwargs)

