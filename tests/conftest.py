import importlib
import os
import pip
import pytest
import shutil
import sys


@pytest.fixture
def pip_mock(mocker):
    yield pip
    importlib.reload(pip)


@pytest.fixture
def poetry_mock(mocker):
    # try to import poetry installed via pip
    try:
        # pylint: disable=import-error
        import poetry
    except ImportError:
        # try to import poetry installed via get-poetry.py
        path = shutil.which("poetry")
        dirname = os.path.dirname(path)
        libdir = f'{dirname}/../lib'
        sys.path.insert(0, libdir)

    # set up relevant mocks
    mocker.patch('poetry.installation.pip_installer.PipInstaller.run')
    mocker.patch('poetry.console.main')

    yield poetry
    importlib.reload(poetry)


@pytest.fixture
def unpatched_run_mock(mocker):
    return mocker.patch(
        'poetry.installation.pip_installer.PipInstaller._unpatched_run')


@pytest.fixture
def sys_exit_mock(mocker):
    return mocker.patch('sys.exit')
