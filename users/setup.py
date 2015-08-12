from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
"""
REQUIREMENTS = [
    'invisibleroads-posts',
    'invisibleroads-records',
    'pyramid_redis_sessions',
    'velruse',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])
setup(
    name='invisibleroads-users',
    version='0.1',
    description='Authentication and authorization',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid :: InvisibleRoads',
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
