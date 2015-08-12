from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[console_scripts]
ir-initialize = invisibleroads_records.scripts.initialize:run
"""
REQUIREMENTS = [
    'dogpile.cache',
    'pyramid',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])
setup(
    name='invisibleroads-records',
    version='0.2',
    description='Database functionality',
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
