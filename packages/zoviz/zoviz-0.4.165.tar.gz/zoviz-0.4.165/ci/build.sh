#!/bin/sh

# Update build env
echo "Building Job $CI_PIPELINE_IID"
apt update -y
apt install -y python3 python3-pip git

# Increment revision
sed -i "s/{ci_build_rev}/$CI_PIPELINE_IID/g" ./zoviz/metadata.py
cat ./zoviz/metadata.py

# Install build packages
pip3 install pylint==2.5.0
pip3 install nose sphinx sphinx_rtd_theme twine lorem
pip3 install --upgrade setuptools wheel
pip3 install -e .

# Build Wheel for deployment to PyPI
python3 setup.py sdist bdist_wheel
