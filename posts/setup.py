from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[paste.app_factory]
main = invisibleroads_posts:main
[pyramid.scaffold]
posts=invisibleroads_posts.scaffolds:PostsTemplate
"""
REQUIREMENTS = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
] + [
    'dogpile.cache',
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
    version='0.1',
    description='Web application defaults',
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
    entry_points=ENTRY_POINTS)
