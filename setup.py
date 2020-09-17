import subprocess
from os.path import abspath, dirname, join
from setuptools import find_packages, setup
# https://stackoverflow.com/a/45021666/192092
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


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
    'invisibleroads-posts >= 0.7.14',
    'invisibleroads-records >= 0.5.8.1',
    # security
    'miscreant',
    # 'pyramid-authsanity',
    'pyramid-redis-sessions',
    'requests-oauthlib',
    # shortcut
    'invisibleroads-macros-configuration >= 1.0.8',
    'invisibleroads-macros-log >= 1.0.3',
    'invisibleroads-macros-security >= 1.0.1',
    # other
]
TEST_REQUIREMENTS = [
    'pytest-cov',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.md', 'CHANGES.md'])


# !!! Remove after pyramid-authsanity merges patch request
PACKAGE_URLS = [
    'https://github.com/invisibleroads/pyramid_authsanity/tarball/patch-1',
]


# https://github.com/BaderLab/saber/issues/35#issuecomment-467827175
class PostInstall(install):

    def run(self):
        super().run()
        print(subprocess.getoutput('pip install ' + ' '.join(PACKAGE_URLS)))


class PostDevelop(develop):

    def run(self):
        super().run()
        print(subprocess.getoutput('pip install ' + ' '.join(PACKAGE_URLS)))


class PostEggInfo(egg_info):

    def run(self):
        super().run()
        print(subprocess.getoutput('pip install ' + ' '.join(PACKAGE_URLS)))


setup(
    name='invisibleroads-users',
    version='0.6.0',
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
    entry_points=ENTRY_POINTS,
    cmdclass={
        'install': PostInstall,
        'develop': PostDevelop,
        'egg_info': PostEggInfo,
    })
