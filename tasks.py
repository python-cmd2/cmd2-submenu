#
# -*- coding: utf-8 -*-
"""Development related tasks to be run with 'invoke'"""

import os
import re
import shutil
import sys

import invoke

# shared function
def rmrf(items, verbose=True):
    "Silently remove a list of directories or files"
    if isinstance(items, str):
        items = [items]

    for item in items:
        if verbose:
            print("Removing {}".format(item))
        shutil.rmtree(item, ignore_errors=True)
        # rmtree doesn't remove bare files
        try:
            os.remove(item)
        except FileNotFoundError:
            pass


# create namespaces
namespace = invoke.Collection()
namespace_clean = invoke.Collection('clean')
namespace.add_collection(namespace_clean, 'clean')

#####
#
# pytest, tox, pylint, and codecov
#
#####
@invoke.task
def pytest(context):
    "Run tests and code coverage using pytest"
    context.run("pytest --cov=cmd2_submenu")
namespace.add_task(pytest)

@invoke.task
def pytest_clean(context):
    "Remove pytest cache and code coverage files and directories"
    #pylint: disable=unused-argument
    dirs = ['.pytest_cache', '.cache', '.coverage']
    rmrf(dirs)
namespace_clean.add_task(pytest_clean, 'pytest')

@invoke.task
def tox(context):
    "Run unit and integration tests on multiple python versions using tox"
    context.run("tox")
namespace.add_task(tox)

@invoke.task
def tox_clean(context):
    "Remove tox virtualenvs and logs"
    #pylint: disable=unused-argument
    rmrf('.tox')
namespace_clean.add_task(tox_clean, 'tox')

@invoke.task
def pylint(context):
    "Check code quality using pylint"
    context.run('pylint --rcfile=cmd2_submenu/pylintrc cmd2_submenu')
namespace.add_task(pylint)

@invoke.task
def pylint_tests(context):
    "Check code quality of test suite using pylint"
    context.run('pylint --rcfile=tests/pylintrc tests')
namespace.add_task(pylint_tests)


#####
#
# build and distribute
#
#####
BUILDDIR = 'build'
DISTDIR = 'dist'

@invoke.task
def build_clean(context):
    "Remove the build directory"
    #pylint: disable=unused-argument
    rmrf(BUILDDIR)
namespace_clean.add_task(build_clean, 'build')

@invoke.task
def dist_clean(context):
    "Remove the dist directory"
    #pylint: disable=unused-argument
    rmrf(DISTDIR)
namespace_clean.add_task(dist_clean, 'dist')

@invoke.task
def eggs_clean(context):
    "Remove egg directories"
    #pylint: disable=unused-argument
    dirs = set()
    dirs.add('.eggs')
    for name in os.listdir(os.curdir):
        if name.endswith('.egg-info'):
            dirs.add(name)
        if name.endswith('.egg'):
            dirs.add(name)
    rmrf(dirs)
namespace_clean.add_task(eggs_clean, 'eggs')

@invoke.task
def bytecode_clean(context):
    "Remove __pycache__ directories and *.pyc files"
    #pylint: disable=unused-argument
    dirs = set()
    for root, dirnames, files in os.walk(os.curdir):
        if '__pycache__' in dirnames:
            dirs.add(os.path.join(root, '__pycache__'))
        for file in files:
            if file.endswith(".pyc"):
                dirs.add(os.path.join(root,file))
    print("Removing __pycache__ directories and .pyc files")
    rmrf(dirs, verbose=False)
namespace_clean.add_task(bytecode_clean, 'bytecode')

#
# make a dummy clean task which runs all the tasks in the clean namespace
clean_tasks = list(namespace_clean.tasks.values())
@invoke.task(pre=list(namespace_clean.tasks.values()), default=True)
def clean_all(context):
    "Run all clean tasks"
    #pylint: disable=unused-argument
    pass
namespace_clean.add_task(clean_all, 'all')


@invoke.task
def tag(context, name, message=''):
    "Add a Git tag and push it to origin"
    # If a tag was provided on the command-line, then add a Git tag and push it to origin
    if name:
        context.run('git tag -a {} -m {!r}'.format(name, message))
        context.run('git push origin {}'.format(name))
namespace.add_task(tag)

@invoke.task()
def validatetag(context):
    "Check to make sure that a tag exists for the current HEAD and it looks like a valid version number"
    # Validate that a Git tag exists for the current commit HEAD
    result = context.run("git describe --exact-match --tags $(git log -n1 --pretty='%h')")
    tag = result.stdout.rstrip()

    # Validate that the Git tag appears to be a valid version number
    ver_regex = re.compile('(\d+)\.(\d+)\.(\d+)')
    match = ver_regex.fullmatch(tag)
    if match is None:
        print('Tag {!r} does not appear to be a valid version number'.format(tag))
        sys.exit(-1)
    else:
        print('Tag {!r} appears to be a valid version number'.format(tag))
namespace.add_task(validatetag)

@invoke.task(pre=[clean_all])
def sdist(context):
    "Create a source distribution"
    context.run('python setup.py sdist')
namespace.add_task(sdist)

@invoke.task(pre=[clean_all])
def wheel(context):
    "Build a wheel distribution"
    context.run('python setup.py bdist_wheel')
namespace.add_task(wheel)

@invoke.task(pre=[validatetag, sdist, wheel])
def pypi(context):
    "Build and upload a distribution to pypi"
    context.run('twine upload dist/*')
namespace.add_task(pypi)

@invoke.task(pre=[validatetag, sdist, wheel])
def pypi_test(context):
    "Build and upload a distribution to https://test.pypi.org"
    context.run('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
namespace.add_task(pypi_test)
