#!/bin/bash

# Configure PyPI
touch ~/.pypirc
echo "\
[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = $PyPI_API_key
" > ~/.pypirc;

# Upload
echo "On branch $CI_COMMIT_BRANCH"
if [[ "$CI_COMMIT_BRANCH" == "master" ]]
then
  { \
    echo "Deploying to PyPI";
    python3 -m twine upload ./dist/*; \
  }
else
echo "Bypassing deployment";
fi
