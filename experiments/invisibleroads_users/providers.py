from pyramid.httpexceptions import HTTPNotFound
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

from .settings import S


class Provider(object):

    authorization_url = ''
    token_url = ''
    resource_url = ''
    scope = []
    fixes = []

    def __init__(self, request, consumer_key, consumer_secret, auth_state):
        redirect_uri = request.route_url(
            'users_enter_callback', provider_name=self.name)
        auth_session = OAuth2Session(
            consumer_key, scope=self.scope, redirect_uri=redirect_uri,
            state=auth_state)
        for fix in self.fixes:
            auth_session = fix(auth_session)
        self.auth_session = auth_session
        self.auth_state = auth_state
        self.consumer_secret = consumer_secret
        self.request_url = request.url

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def auth_url(self):
        return self.auth_session.authorization_url(self.authorization_url)[0]

    @property
    def user_definition(self):
        self.auth_session.fetch_token(
            self.token_url, client_secret=self.consumer_secret,
            authorization_response=self.request_url)
        response = self.auth_session.get(self.resource_url)
        resource_definition = response.json()
        return self.get_user_definition(resource_definition)


class Google(Provider):

    authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    token_url = 'https://www.googleapis.com/oauth2/v4/token'
    resource_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    scope = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid',
    ]

    def get_user_definition(self, d):
        return {
            'name': d['name'],
            'email': d['email'],
            'image_url': d['picture'],
        }


class LinkedIn(Provider):

    authorization_url = 'https://www.linkedin.com/uas/oauth2/authorization'
    token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
    resource_url = (
        'https://api.linkedin.com/v1/people/~'
        ':(formattedName,emailAddress,pictureUrl)?format=json')
    fixes = [
        linkedin_compliance_fix,
    ]

    def get_user_definition(self, d):
        return {
            'name': d['formattedName'],
            'email': d['emailAddress'],
            'image_url': d['pictureUrl'],
        }


def get_provider(request, auth_state):
    matchdict = request.matchdict
    provider_name = matchdict['provider_name']
    try:
        provider_definition = S['provider_definitions'][provider_name]
    except KeyError:
        raise HTTPNotFound({'provider_name': 'bad'})
    return CLASS_BY_NAME[provider_name](
        request,
        provider_definition['consumer_key'],
        provider_definition['consumer_secret'],
        auth_state)


CLASS_BY_NAME = {
    'google': Google,
    'linkedin': LinkedIn,
}
