import importlib
import os
import pip
import pytest
import shutil
import sys


@pytest.fixture
def add_poetry_to_libdir():
    path = shutil.which("poetry")
    dirname = os.path.dirname(path)
    libdir = f'{dirname}/../lib'

    sys.path.insert(0, libdir)
    print(f'DEBUG here is poetry libdir contents "{os.listdir(libdir)}"')
    raise Exception()


@pytest.fixture
def pip_mock(mocker):
    yield pip
    importlib.reload(pip)


@pytest.fixture
def poetry_mock(mocker, add_poetry_to_libdir):
    # pylint: disable=import-error
    import poetry
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
