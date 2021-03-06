[![Python JHeaps](https://github.com/d-michail/python-jheaps/actions/workflows/master.yml/badge.svg)](https://github.com/d-michail/python-jheaps/actions/workflows/master.yml)

# Python-JHeaps

Python bindings for the  [JHeaps library](https://www.jheaps.org/).

The JHeaps is a free Java library that provides various heap implementations.

While the original library is written in Java, this package uses a *native build* provided by
the [jheaps-capi](https://github.com/d-michail/jheaps-capi) project. The native build is in the form of a 
shared library, created by [GraalVM](https://www.graalvm.org/).

The result is a *native self-contained library* with *no dependency* on the JVM!

## Installing

We automatically build 64-bit wheels for python versions 3.6, 3.7, and 3.8 on Linux,
Windows and MacOSX. They can be directly downloaded from [PyPI](https://pypi.org/project/jheaps/)
or using pip.
For linux we use [PEP 571](https://www.python.org/dev/peps/pep-0571/)
which means that pip version must be `>= 19.0`.

Thus, on a recent machine, installation should be as easy as:

```
pip install jheaps
```

If your pip version is older than `19.0` you will need to upgrade: 

```
pip install --upgrade pip
pip install jheaps
```

If you want to use `virtualenv` or `venv` module, you can write:

```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install jheaps
```

Installation on the user directory is also possible:

```
pip install --upgrade pip
pip install --user jheaps
```

## Documentation 

Automatically generated documentation with a tutorial and examples can be found at 
<https://python-jheaps.readthedocs.io/>. This includes full API docs, tutorials and examples.

## Building

The jheaps-capi project is included in the sources as a git submodule in folder `vendor/source/jheaps-capi`.
You need to either initialize the submodule by hand, or you can pass option `--recurse-submodules` when 
cloning this repository.

The following pieces of software are required for the build to succeed:

 * GraalVM 20.0 with Java 11 support
 * Native Image component from GraalVM
 * Maven Java build tool
 * GNU C compiler or clang
 * CMake 
 * Python 3.6 and above
 * SWIG 3 and above

If all the above are installed properly, building can be done using

```
python setup.py build
```

For Windows you will need Microsoft Visual C++ (MSVC) 2017 15.5.5 or later. Build the
system using the proper
[Developer Command Prompt](https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=vs-2019#developer_command_prompt_shortcuts)
for your version of [Visual Studio](https://visualstudio.microsoft.com/vs/). This means
`x64 Native Tools Command Prompt`. Use Visual Studio 2017 or later.

## Install

Install using 

```
pip install .
```

## Develop

Since the library contains parts which are written in C that need to be compiled before use, make sure you have 
the necessary compilers and development headers installed. Compiled code means that additional steps are required
in order to import from the development sources. Using the following commands you can setup an in-place development 
environment:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This allows you to import the in-place build from the repository base directory. If you want it to 
also be visible outside the base dir, you have to adjust the `PYTHONPATH` accordingly.
Note also that the above commands call `python setup.py develop`. Instead of adjusting PYTHONPATH, this installs
a .egg-link file into your site-packages as well as adjusts the easy-install.pth there, so its a more permanent
operation.

## Tests

Execute the tests by giving

```
pip install -r requirements/test.txt
pytest
```

## Building the docs

```
pip install -r requirements/doc.txt
cd docs && make html
```

## License

This library may be used under the terms of the

 * Apache License 2.0
   https://www.apache.org/licenses/LICENSE-2.0

Please note that this library is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Please refer to the license for details.

SPDX-License-Identifier: Apache-2.0

## Author

(C) Copyright 2020, by Dimitrios Michail

Enjoy!
