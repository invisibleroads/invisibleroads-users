def includeme(config):
    config.add_route(
        'authorizations.json',
        '/authorizations.json')
    config.add_route(
        'authorizations_enter',
        '/authorizations/enter/{providerName}')
    config.add_route(
        'authorizations_enter_callback',
        '/authorizations/enter/{providerName}/callback')
    config.add_route(
        'authorizations_leave',
        '/authorizations/leave')
