InvisibleRoads Users
====================
Add authentication and authorization.

    config.include('invisibleroads_users')

Use
---
Prepare environment.

    VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv $VIRTUAL_ENV
    source $VIRTUAL_ENV/bin/activate

    NODE_PATH=$VIRTUAL_ENV/lib/node_modules
    npm install -g browserify gulp gulp-if gulp-uglify vinyl-transform yargs

Install package.

    cd ~/Documents/invisibleroads-users/node_modules/invisibleroads-users
    npm install -g

    cd ~/Documents/invisibleroads-users
    python setup.py develop
    gulp --production
