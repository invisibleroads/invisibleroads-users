from dogpile.cache.api import NO_VALUE
from dogpile.cache.region import make_region
from dogpile.cache.util import sha1_mangle_key
from invisibleroads_macros.config import get_interpretation_by_name
from sqlalchemy.orm.interfaces import MapperOption
from sqlalchemy.orm.query import Query


CACHE_BACKEND = 'memory'
CACHE_EXPIRATION_TIME = 3600
CACHE_REGIONS = {}
KEY_MANGLERS = {
    'sha1': sha1_mangle_key,
}


class CachingQuery(Query):

    def __init__(self, cache_regions, *args, **kw):
        self._cache_regions = cache_regions
        super(CachingQuery, self).__init__(*args, **kw)

    def get_value(self, make_value):
        value = self._cache_region.get_or_create(self._cache_key, make_value)
        if value is NO_VALUE:
            raise KeyError(self._cache_key)
        value = self.merge_result(value, load=False)
        return self.expunge_result(value)

    def set_value(self, value):
        self._cache_region.set(self._cache_key, value)

    def invalidate(self):
        self._cache_region.delete(self._cache_key)

    def expunge_result(self, value):
        vs = []
        db = self.session
        for v in value:
            db.expunge(v)
            vs.append(v)
        return iter(vs)

    @property
    def _cache_region(self):
        if not hasattr(self, '__cache_region'):
            cache_region_name = self._from_cache.cache_region_name
            self.__cache_region = self._cache_regions[cache_region_name]
        return self.__cache_region

    @property
    def _cache_key(self):
        if not hasattr(self, '__cache_key'):
            cache_key = self._from_cache.cache_key
            self.__cache_key = cache_key or self._make_cache_key()
        return self.__cache_key

    def _make_cache_key(self):
        compiled = self.with_labels().statement.compile()
        params = compiled.params
        return ' '.join(
            [str(compiled)] +
            [str(params[k]) for k in sorted(params)])

    def __iter__(self):
        if hasattr(self, '_from_cache'):
            make_value = lambda: list(super(CachingQuery, self).__iter__())
            return self.get_value(make_value)
        else:
            return super(CachingQuery, self).__iter__()


class FromCache(MapperOption):

    propagate_to_loaders = False

    def __init__(self, cache_region_name='sqlalchemy', cache_key=None):
        self.cache_region_name = cache_region_name
        self.cache_key = cache_key

    def process_query(self, query):
        query._from_cache = self


def configure_cache(config, prefix='cache.'):
    settings = config.registry.settings
    interpretation = get_interpretation_by_name(
        settings, prefix, interpret_cache_setting)
    for region_name, region_settings in interpretation.iteritems():
        key_mangler = region_settings.pop(
            'key_mangler', None)
        backend = 'dogpile.cache.' + region_settings.pop(
            'backend', CACHE_BACKEND)
        expiration_time = int(region_settings.pop(
            'expiration_time', CACHE_EXPIRATION_TIME))
        CACHE_REGIONS[region_name] = make_region(
            key_mangler=key_mangler,
        ).configure(backend, expiration_time, arguments=region_settings)


def interpret_cache_setting(attribute, value):
    if 'key_mangler' == attribute:
        return {'key_mangler': KEY_MANGLERS[value]}
    return {attribute: value}


def make_query_factory(*args, **kw):
    return CachingQuery(CACHE_REGIONS, *args, **kw)
