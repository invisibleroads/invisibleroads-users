from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = '''
'''
APPLICATION_CLASSIFIERS = [
    'Programming Language :: Python',
    'Framework :: Pyramid',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'License :: OSI Approved :: MIT License',
]
APPLICATION_REQUIREMENTS = [
    # web
    'pyramid',
    # database
    'redis',
    'sqlalchemy',
    # architecture
    'invisibleroads-posts >= 0.7.15',
    'invisibleroads-records >= 0.5.9',
    # security
    'miscreant',
    'pyramid-authsanity',
    'pyramid-redis-sessions',
    'requests-oauthlib',
    # shortcut
    'invisibleroads-macros-configuration >= 1.0.8',
    'invisibleroads-macros-log >= 1.0.3',
    'invisibleroads-macros-security >= 1.0.1',
]
TEST_REQUIREMENTS = [
    'pytest-cov',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.md', 'CHANGES.md'])


setup(
    name='invisibleroads-users',
    version='0.6.2',
    description='Web application security defaults',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=APPLICATION_CLASSIFIERS,
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='https://github.com/invisibleroads/invisibleroads-users',
    keywords='web wsgi bfg pylons pyramid invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    extras_require={'test': TEST_REQUIREMENTS},
    install_requires=APPLICATION_REQUIREMENTS,
    entry_points=ENTRY_POINTS)
