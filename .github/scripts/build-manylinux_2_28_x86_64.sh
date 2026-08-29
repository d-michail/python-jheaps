#!/bin/bash
set -e -x

echo "Current dir: `pwd`"
echo "GITHUB_WORKSPACE: $GITHUB_WORKSPACE"

# Build wheels for Python 3.10, 3.11, 3.12, 3.13, 3.14
# Although we have a manylinux compatible wheel generated directly from
# setup.py, PyPI requires that the platform tag is set to a manylinux one
# (e.g. manylinux_2_28_x86_64 instead of linux_x86_64).
# Because auditwheel repair unecessarily bundles in zlib and breaks our
# RPATH we don't use it, instead we directly specify the tag with --plat-name
PYVERSIONS="310 311 312 313 314"

for V in $PYVERSIONS; do
    PYBIN=/opt/python/cp${V}-cp${V}/bin
    "${PYBIN}/pip" install --upgrade pip setuptools wheel
    "${PYBIN}/python" setup.py bdist_wheel --plat-name=manylinux_2_28_x86_64
done

# Show if our wheels are consistent with auditwheel (they should be)
for WHL in dist/*.whl
do
    auditwheel show "$WHL"
done

# Generate source distribution with sdist so we can upload it to PyPI
/opt/python/cp312-cp312/bin/python setup.py sdist

# Install generated wheels and run the tests
for V in $PYVERSIONS; do
    PYBIN=/opt/python/cp${V}-cp${V}/bin
    "${PYBIN}/pip" install -r requirements/test.txt
    "${PYBIN}/pip" install jheaps --no-index -f $GITHUB_WORKSPACE/dist
    "${PYBIN}/pytest"
done
