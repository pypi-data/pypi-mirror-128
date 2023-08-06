from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include("pyramid_beaker")
        config.include("pyramid_chameleon")
        config.include("chisel")
        config.include('.models')
        config.include('.routes')
        config.include('.security')
        config.include('.events')
        config.include('.render')
        config.include('.translations')
        config.scan()
    return config.make_wsgi_app()
