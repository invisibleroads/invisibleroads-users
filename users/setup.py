from os.path import abspath, dirname, join
from setuptools import setup, find_packages


ENTRY_POINTS = """
"""
REQUIREMENTS = [
    'invisibleroads_posts',
    'invisibleroads_records',
    'pyramid_redis_sessions',
]


HERE = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(HERE, _)).read() for _ in [
    'README.md',
    'CHANGES.md',
])
setup(
    name='invisibleroads-users',
    version='0.1',
    description='Authentication and authorization',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Framework :: Pyramid :: InvisibleRoads',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='http://invisibleroads.com',
    keywords='web pyramid pylons invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS,
    test_suite='invisibleroads_users',
    entry_points=ENTRY_POINTS,
)
