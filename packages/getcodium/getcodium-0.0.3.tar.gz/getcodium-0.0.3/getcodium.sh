#!/usr/bin/bash

_args=("$@") # all parameters from terminal.

p8(){
    isort ./setup.py
    autopep8 -i -a -a -r -v ./setup.py
    isort ./getcodium/__init__.py
    autopep8 -i -a -a -r -v ./getcodium/__init__.py
    isort ./getcodium.py
    autopep8 -i -a -a -r -v ./getcodium.py
}


twine_upload(){
    twine upload  dist/*
}

bdist(){
    rm -rf dist/ build/ getcodium.egg-info/
    python3 setup.py sdist bdist_wheel
}

_i_test(){
    bdist
    pip3 uninstall getcodium -y
    pip3 install dist/*.whl
    getcodium
}

tu(){       twine_upload;       }
its(){      _i_test;           }
bdup(){     bdist; tu;          }

${_args[0]}
