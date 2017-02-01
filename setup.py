import sys
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])


for command in ('register', 'upload'):
    if command in sys.argv:
        exit('cannot %s private repository' % command)


setup(
    name='invisibleroads-users',
    version='0.3.2',
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
    keywords='web wsgi bfg pylons pyramid invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'pytest-runner'
    ],
    install_requires=[
        'invisibleroads-posts>=0.5.2',
        'invisibleroads-records>=0.4.0',
        'pyramid-redis-sessions',
        'velruse',
    ])
