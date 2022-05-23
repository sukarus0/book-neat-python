#!/bin/bash

required_pkg='SQLAlchemy mysql-connector-python'
pkg_list=($required_pkg)

for package in ${pkg_list[@]};
do
        if [ -z "$(pip list | grep -i ${package})" ]; then
                pip install ${package}
        else
                echo "${package} already installed"
        fi
done

export FLASK_APP=app
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=5000
