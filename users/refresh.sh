#!/bin/bash
MODULE_NAMES="invisibleroads_posts invisibleroads_users"
for MODULE_NAME in ${MODULE_NAMES}; do
    ROOT_FOLDER=`python -c "import ${MODULE_NAME}; from os.path import abspath as a, dirname as d; print(d(d(a(${MODULE_NAME}.__file__))))"`
    NODE_FOLDER=${ROOT_FOLDER}/node_modules/${MODULE_NAME/_/-}
    PYTHON_FOLDER=${ROOT_FOLDER}/${MODULE_NAME}
    pushd ${NODE_FOLDER} > /dev/null; npm install -g; popd > /dev/null
    if [[ "$1" == "--debug" || "$1" == "-d" ]]; then
        JS=`browserify ${NODE_FOLDER}/library.js`
    else
        JS=`browserify ${NODE_FOLDER}/library.js | uglifyjs -c`
    fi
    echo "$JS" > ${PYTHON_FOLDER}/assets/library.js
done
