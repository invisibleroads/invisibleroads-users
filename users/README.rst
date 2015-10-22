InvisibleRoads Users
====================
Add authentication and authorization. ::

    config.include('invisibleroads_users')


Use
---
Prepare environment. ::

    export VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv ${VIRTUAL_ENV}
    source ${VIRTUAL_ENV}/bin/activate

    export NODE_PATH=${VIRTUAL_ENV}/lib/node_modules
    npm install -g browserify uglify-js

Install package. ::

    PYTHON_PACKAGE_FOLDER=~/Projects/invisibleroads-packages/users
    NODE_PACKAGE_FOLDER=${PACKAGE_FOLDER}/node_modules/invisibleroads-users

    cd ${PYTHON_PACKAGE_FOLDER}
    python setup.py develop
    bash refresh.sh

    cd ${NODE_PACKAGE_FOLDER}
    npm install -g
