from os.path import abspath, dirname, join
from setuptools import setup, find_packages


ENTRY_POINTS = """
[paste.app_factory]
main = invisibleroads_posts:main
"""
REQUIREMENTS = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
] + [
    'mistune',
    'pyramid_mako',
    'titlecase',
]


HERE = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(HERE, _)).read() for _ in [
    'README.md',
    'CHANGES.md',
])
setup(
    name='invisibleroads-posts',
    version='0.0.0',
    description='invisibleroads-posts',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Framework :: Pyramid :: InvisibleRoads',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='http://invisibleroads.com',
    keywords='web pyramid pylons invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS,
    test_suite='invisibleroads_posts',
    entry_points=ENTRY_POINTS,
)
