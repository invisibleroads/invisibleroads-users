from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[console_scripts]
ir-initialize = invisibleroads_records.scripts.initialize:main
"""
REQUIREMENTS = [
    'pyramid',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
]


HERE = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(HERE, _)).read() for _ in [
    'README.md',
    'CHANGES.md',
])
setup(
    name='invisibleroads-records',
    version='0.1',
    description='Database functionality',
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
    test_suite='invisibleroads_records',
    entry_points=ENTRY_POINTS)
