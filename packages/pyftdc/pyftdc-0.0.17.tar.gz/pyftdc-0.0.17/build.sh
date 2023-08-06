#!/bin/bash

rm -fr dist/*
python setup.py bdist_wheel
python setup.py sdist
VER=`sed "s/\"//g"  _version.py | sed "s/ //g" | cut -d '=' -f 2`

PLATFORM=`uname`
case $PLATFORM in
 "Linux")
   pip install --force-reinstall dist/pyftdc-${VER}-*linux*.whl
   ;;
  "Darwin")
  pip install --force-reinstall dist/pyftdc-${VER}-*macosx*.whl
  ;;
esac
