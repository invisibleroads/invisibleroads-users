invisibleroads-posts
====================
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


Recreate package
----------------
- [Pyramid](http://docs.pylonsproject.org/en/latest/docs/pyramid.html) 1.6dev
- [Bootstrap](http://getbootstrap.com) 3.3.2
- [JQuery](http://jquery.com) 1.11.2
- [RequireJS](http://requirejs.org) 2.1.15
