def includeme(config):
    config.add_route(
        'authorizations.json',
        '/authorizations.json')
    config.add_route(
        'authorizations_enter',
        '/authorizations/enter/{provider_name}')
    config.add_route(
        'authorizations_enter_callback',
        '/authorizations/enter/{provider_name}/callback')
    config.add_route(
        'authorizations_leave',
        '/authorizations/leave')
