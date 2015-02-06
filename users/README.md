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
    npm install -g requirejs

Install package.

    cd ~/Documents/invisibleroads-users
    r.js -o build.js

    cd ~/Experiments/invisibleroads-users
    python setup.py develop
