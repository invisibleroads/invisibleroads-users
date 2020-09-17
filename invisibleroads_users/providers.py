from pyramid.httpexceptions import HTTPNotFound
from requests_oauthlib import OAuth2Session

from .constants import S


class AuthProvider(object):

    def __init__(
            self, request, auth_state, auth_scopes, consumer_key,
            consumer_secret, form_url, token_url, resource_url,
            compliance_fixes):
        redirect_uri = request.route_url(
            'authorizations_enter_callback', provider_name=self.name)
        auth_session = OAuth2Session(
            consumer_key,
            scope=auth_scopes,
            redirect_uri=redirect_uri,
            state=auth_state)
        for f in compliance_fixes:
            auth_session = f(auth_session)
        self._consumer_secret = consumer_secret
        self._form_url = form_url
        self._token_url = token_url
        self._resource_url = resource_url
        self._auth_session = auth_session
        self._request_url = request.url

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def form_url(self):
        return self._auth_session.authorization_url(self._form_url)[0]

    def get_user_definition(self):
        d = self._auth_session.fetch_token(
            self._token_url,
            client_secret=self._consumer_secret,
            authorization_response=self._request_url,
            verify=S['verify_tls'])
        access_token = d['access_token']
        refresh_token = d.get('refresh_token')
        response = self._auth_session.get(self._resource_url)
        resource_definition = response.json()
        return self._get_user_definition(
            resource_definition, access_token, refresh_token)


class Google(AuthProvider):

    def _get_user_definition(
            self, resource_definition, access_token, refresh_token):
        return {
            'name': resource_definition['name'],
            'email': resource_definition['email'],
            'image_url': resource_definition['picture'],
        }


'''
# TODO: Fix
# https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/profile-picture

class LinkedIn(AuthProvider):

    def _get_user_definition(
            self, resource_definition, access_token, refresh_token):
        first_name = resource_definition['localizedFirstName']
        last_name = resource_definition['localizedLastName']
        return {
            'name': f'{first_name} {last_name}',
            'email': resource_definition['emailAddress'],
            'image_url': resource_definition['profilePicture']['displayImage'],
        }
'''


def get_auth_provider(request, auth_state):
    matchdict = request.matchdict
    provider_name = matchdict['provider_name']
    try:
        provider_definition = S['provider_definitions'][provider_name]
    except KeyError:
        raise HTTPNotFound({'provider_name': 'is invalid'})
    return PROVIDER_BY_NAME[provider_name](
        request, auth_state, **provider_definition)


def get_enter_url_by_name(request):
    return {provider_name: request.route_url(
        'authorizations_enter',
        provider_name=provider_name,
    ) for provider_name in S['provider_definitions']}


PROVIDER_BY_NAME = {
    'google': Google,
    # 'linkedin': LinkedIn,
}
