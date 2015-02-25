from dogpile.cache import make_region


function_cache = make_region()


def configure_cache(config, prefix='cache.'):
    settings = config.registry.settings
    function_cache.configure_from_config(settings, prefix + 'function.')
