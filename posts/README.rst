InvisibleRoads Posts
====================
Posts form the foundation for most of our web applications.

- [Pyramid](http://docs.pylonsproject.org/en/latest/docs/pyramid.html) 1.5.7
- [Bootstrap](http://getbootstrap.com) 3.3.5
- [JQuery](http://jquery.com) 1.11.3


Use
---
Prepare environment.

    VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv ${VIRTUAL_ENV}
    source ${VIRTUAL_ENV}/bin/activate

    NODE_PATH=${VIRTUAL_ENV}/lib/node_modules
    npm install -g browserify uglify-js

Install package.

    PACKAGE_FOLDER=~/Projects/invisibleroads-packages/posts

    cd ~/Projects
    git clone git@github.com:invisibleroads/invisibleroads-posts.git

    cd ${PACKAGE_FOLDER}
    python setup.py develop

    cd ${PACKAGE_FOLDER}/node_modules/invisibleroads-posts
    npm install -g

Create project.

    cd ~/Projects
    pcreate -s posts xyz

Install project.

    cd ~/Projects/xyz
    python setup.py develop

Launch development server.

    mkdir -p xyz/assets
    browserify node_modules/xyz/base.js > xyz/assets/base.js
    pserve development.ini

Launch production server.

    mkdir -p xyz/assets
    browserify node_modules/xyz/base.js | uglifyjs -c > xyz/assets/base.js
    pserve production.ini


Recreate
--------
Use starter scaffold.

    cd ~/Experiments
    pcreate -s starter invisibleroads-posts
    SOURCE_FOLDER=~/Projects/invisibleroads-posts
    TARGET_FOLDER=~/Experiments/invisibleroads-posts

Add .gitignore.

    wget https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore -O ${TARGET_FOLDER}/.gitignore
    vimdiff ${TARGET_FOLDER}/.gitignore ${SOURCE_FOLDER}/.gitignore

Update configuration files.

    vimdiff ${TARGET_FOLDER}/MANIFEST.in ${SOURCE_FOLDER}/MANIFEST.in

    mv ${TARGET_FOLDER}/CHANGES.{txt,rst}
    vimdiff ${TARGET_FOLDER}/CHANGES.rst ${SOURCE_FOLDER}/CHANGES.rst

    mv ${TARGET_FOLDER}/README.{txt,rst}
    vimdiff ${TARGET_FOLDER}/README.rst ${SOURCE_FOLDER}/README.rst

    vimdiff ${TARGET_FOLDER}/development.ini ${SOURCE_FOLDER}/development.ini
    vimdiff ${TARGET_FOLDER}/production.ini ${SOURCE_FOLDER}/production.ini

    vimdiff ${TARGET_FOLDER}/setup.py ${SOURCE_FOLDER}/setup.py

Update package files.

    vimdiff ${TARGET_FOLDER}/invisibleroads_posts/__init__.py ${SOURCE_FOLDER}/invisibleroads_posts/__init__.py
    vimdiff ${TARGET_FOLDER}/invisibleroads_posts/views.py ${SOURCE_FOLDER}/invisibleroads_posts/views.py
    rm ${TARGET_FOLDER}/invisibleroads_posts/tests.py

Prepare templates.

    TEMPLATES_FOLDER=${TARGET_FOLDER}/invisibleroads_posts/templates
    rm ${TARGET_FOLDER}/invisibleroads_posts/templates/*
    mkdir ${TEMPLATES_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/templates/* ${TEMPLATES_FOLDER}
    vim ${TEMPLATES_FOLDER}/base.jinja2
    vim ${TEMPLATES_FOLDER}/posts.jinja2

Prepare assets.

    ASSETS_FOLDER=${TARGET_FOLDER}/invisibleroads_posts/assets
    rm ${TARGET_FOLDER}/invisibleroads_posts/static/*
    mv ${TARGET_FOLDER}/invisibleroads_posts/static ${ASSETS_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/assets/favicon.ico ${ASSETS_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/assets/robots.txt ${ASSETS_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/assets/whoops.html ${ASSETS_FOLDER}
    cd ${TARGET_FOLDER}
    # browserify node_modules/invisibleroads-posts/base.js > invisibleroads_posts/assets/base.js
    browserify node_modules/invisibleroads-posts/base.js | uglifyjs -c > invisibleroads_posts/assets/base.js

Add [Bootstrap](http://getbootstrap.com).

    BOOTSTRAP_VERSION=3.3.5
    cd ~/Documents
    wget https://github.com/twbs/bootstrap/releases/download/v$BOOTSTRAP_VERSION/bootstrap-$BOOTSTRAP_VERSION-dist.zip
    unzip bootstrap-${BOOTSTRAP_VERSION}-dist.zip
    cd ~/Documents/bootstrap-${BOOTSTRAP_VERSION}-dist
    cp css/bootstrap.min.css ${ASSETS_FOLDER}
    cp js/bootstrap.min.js ${ASSETS_FOLDER}

Add [JQuery](http://jquery.com).

    JQUERY_VERSION=1.11.3
    cd ${ASSETS_FOLDER}
    wget http://code.jquery.com/jquery-${JQUERY_VERSION}.min.js -O jquery.min.js
