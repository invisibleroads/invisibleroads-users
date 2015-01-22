InvisibleRoads posts
====================
Posts form the foundation for most of our web applications.

- [Pyramid](http://docs.pylonsproject.org/en/latest/docs/pyramid.html) 1.6.dev0
- [Bootstrap](http://getbootstrap.com) 3.3.2
- [JQuery](http://jquery.com) 1.11.2
- [RequireJS](http://requirejs.org) 2.1.15


Use
---
Prepare environment.

    VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv $VIRTUAL_ENV
    source $VIRTUAL_ENV/bin/activate

Install package.

    cd ~/Documents
    git clone git@github.com:invisibleroads/invisibleroads-posts.git
    cd ~/Documents/invisibleroads-posts
    python setup.py develop

Create project.

    cd ~/Projects
    pcreate -s invisibleroads our-home
    cd ~/Projects/our-home
    python setup.py develop

Launch server.
    
    cd ~/Projects/our-home
    pserve development.ini


Recreate
--------
Update [Pyramid](http://docs.pylonsproject.org/en/latest/docs/pyramid.html).

    v; pip uninstall pyramid
    cd ~/Documents
    git clone https://github.com/Pylons/pyramid.git
    cd ~/Documents/pyramid
    v; python setup.py develop

Use starter scaffold.

    cd ~/Experiments
    pcreate -s starter invisibleroads-posts
    SOURCE_FOLDER=~/Projects/invisibleroads-posts
    TARGET_FOLDER=~/Experiments/invisibleroads-posts

Add .gitignore.

    wget https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore -O $TARGET_FOLDER/.gitignore
    vimdiff $TARGET_FOLDER/.gitignore $SOURCE_FOLDER/.gitignore

Add CHANGES.md.

    mv $TARGET_FOLDER/CHANGES.{txt,md}
    vimdiff $TARGET_FOLDER/CHANGES.md $SOURCE_FOLDER/CHANGES.md

Add MANIFEST.in.

    vimdiff $TARGET_FOLDER/MANIFEST.in $SOURCE_FOLDER/MANIFEST.in

Add README.md.

    mv $TARGET_FOLDER/README.{txt,md}
    vimdiff $TARGET_FOLDER/README.md $SOURCE_FOLDER/README.md

Add development.ini.

    vimdiff $TARGET_FOLDER/development.ini $SOURCE_FOLDER/development.ini

Add production.ini.

    vimdiff $TARGET_FOLDER/production.ini $SOURCE_FOLDER/production.ini

Add setup.py

    vimdiff $TARGET_FOLDER/setup.py $SOURCE_FOLDER/setup.py

Add __init__.py.

    vimdiff $TARGET_FOLDER/invisibleroads_posts/setup.py $SOURCE_FOLDER/invisibleroads_posts/setup.py

Prepare views.

    VIEWS_FOLDER=$TARGET_FOLDER/invisibleroads_posts/views
    rm $TARGET_FOLDER/invisibleroads_posts/views.py
    mkdir $VIEWS_FOLDER
    cp $SOURCE_FOLDER/invisibleroads_posts/views/__init__.py $VIEWS_FOLDER
    vim $VIEWS_FOLDER/__init__.py

Prepare templates.

    TEMPLATES_FOLDER=$TARGET_FOLDER/invisibleroads_posts/templates
    rm $TARGET_FOLDER/invisibleroads_posts/templates/*
    mkdir $TEMPLATES_FOLDER
    cp $SOURCE_FOLDER/invisibleroads_posts/templates/* $TEMPLATES_FOLDER
    vim $TEMPLATES_FOLDER/base.mako

Prepare assets.

    ASSETS_FOLDER=$TARGET_FOLDER/invisibleroads_posts/assets
    rm $TARGET_FOLDER/invisibleroads_posts/static/*
    mv $TARGET_FOLDER/invisibleroads_posts/static $ASSETS_FOLDER
    vim $ASSETS_FOLDER/common.js

Add favicon.ico.

    cp $SOURCE_FOLDER/invisibleroads_posts/assets/favicon.ico $ASSETS_FOLDER

Add [Bootstrap](http://getbootstrap.com).

    BOOTSTRAP_VERSION=3.3.2
    cd ~/Documents
    wget https://github.com/twbs/bootstrap/releases/download/v$BOOTSTRAP_VERSION/bootstrap-$BOOTSTRAP_VERSION-dist.zip
    unzip bootstrap-$BOOTSTRAP_VERSION-dist.zip
    cd ~/Documents/bootstrap-$BOOTSTRAP_VERSION-dist
    cp css/bootstrap.min.css $ASSETS_FOLDER
    cp css/bootstrap-theme.min.css $ASSETS_FOLDER
    cp js/bootstrap.min.js $ASSETS_FOLDER

Add [JQuery](http://jquery.com).

    JQUERY_VERSION=1.11.2
    cd $ASSETS_FOLDER
    wget http://code.jquery.com/jquery-1.11.2.min.js -O jquery.min.js
    wget http://code.jquery.com/jquery-1.11.2.min.map -O jquery.min.map
    
Add [RequireJS](http://requirejs.org).

    REQUIREJS_VERSION=2.1.15
    cd $ASSETS_FOLDER
    wget http://requirejs.org/docs/release/2.1.15/minified/require.js -O require.min.js
    v; npm install -g requirejs

Add robots.txt.

    cp $SOURCE_FOLDER/invisibleroads_posts/assets/robots.txt $ASSETS_FOLDER

Add whoops.html.

    cp $SOURCE_FOLDER/invisibleroads_posts/assets/whoops.html $ASSETS_FOLDER
    vim $ASSETS_FOLDER/whoops.html

Clean files.

    rm $TARGET_FOLDER/invisibleroads_posts/tests.py
