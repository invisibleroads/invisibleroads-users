# InvisibleRoads Users

This package adds security functionality to your pyramid web service.

## Use

Install dependencies.

    pip install -U cookiecutter

Initialize project.

    cookiecutter https://github.com/invisibleroads/invisibleroads-cookiecutter

Follow the instructions in the generated README.

## Test

    git clone https://github.com/invisibleroads/invisibleroads-users
    cd invisibleroads-users
    pip install -e .[test]
    pytest --cov=invisibleroads_users --cov-report term-missing tests
