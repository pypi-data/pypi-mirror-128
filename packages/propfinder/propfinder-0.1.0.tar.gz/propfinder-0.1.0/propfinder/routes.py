from chisel.routes import create_crud_routes


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(
        'deform_static',
        'deform:static',
        cache_max_age=3600
    )
    config.add_static_view(
        'chisel_static',
        'chisel:static',
        cache_max_age=3600
    )

    # Home
    config.add_route(
        'home',
        '/',
        factory='propfinder.resources.PageResource',
        request_method="GET"
    )

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # Users
    create_crud_routes(
        config,
        'users',
        factory='propfinder.resources.UserResource'
    )

    # Locations
    create_crud_routes(
        config,
        'locations',
        factory='propfinder.resources.LocationResource'
    )
    config.add_route(
        'locations.values',
        'locations/{id}/values',
        factory='propfinder.resources.LocationResource',
        request_method="GET"
    )

    # URLs
    create_crud_routes(
        config,
        'urls',
        factory='propfinder.resources.URLResource'
    )

    # Properties
    create_crud_routes(
        config,
        'properties',
        factory='propfinder.resources.PropertyResource'
    )
    config.add_route(
        'properties.price_changes',
        'properties/{id}/price_changes',
        factory='propfinder.resources.PropertyResource',
        request_method="GET"
    )
    config.add_route(
        'properties.toggle_starred',
        'properties/{id}/toggle_starred',
        factory='propfinder.resources.PropertyResource',
        request_method="POST"
    )
    config.add_route(
        'properties.join',
        'properties/{id}/join',
        factory='propfinder.resources.PropertyResource'
    )

