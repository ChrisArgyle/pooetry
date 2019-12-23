from pooetry import main as pooetry
import pytest
import sys


def test_main__should_patch_poetry__when_pip_and_poetry_are_supported_versions(pip_mock, poetry_mock):
    # change pip version to 19.0.3
    pip_mock.__version__ = "19.0.3"

    # change poetry version to 0.12.17
    poetry_mock.__version__ = "0.12.17"

    # call main
    pooetry.main()

    # assert poetry is patched
    assert poetry_mock.installation.pip_installer.PipInstaller.run == pooetry.run_patch


def test_main__should_not_patch_poetry__when_pip_is_unsupported_version(pip_mock, poetry_mock):
    # change pip version to 10.0.1
    pip_mock.__version__ = "10.0.1"

    # change poetry version to 0.12.17
    poetry_mock.__version__ = "0.12.17"

    # call main
    pooetry.main()

    # assert poetry is not patched
    assert poetry_mock.installation.pip_installer.PipInstaller.run != pooetry.run_patch


def test_main__should_not_patch_poetry__when_poetry_is_unsupported_version(pip_mock, poetry_mock):
    # change pip version to 19.0.3
    pip_mock.__version__ = "19.0.3"

    # change poetry version to 1.0.0b1
    poetry_mock.__version__ = "1.0.0b1"

    # call main
    pooetry.main()

    # assert poetry is not patched
    assert poetry_mock.installation.pip_installer.PipInstaller.run != pooetry.run_patch


def test_main__should_not_patch_poetry__when_pip_is_not_found(mocker, poetry_mock):
    # mock sys.modules to make `import pip` raise an exception
    mocker.patch.dict(sys.modules, {'pip': None})

    # call main
    pooetry.main()

    # assert poetry is not patched
    assert poetry_mock.installation.pip_installer.PipInstaller.run != pooetry.run_patch


def test_main__should_return_error__when_poetry_is_not_found(mocker, sys_exit_mock):
    # patch shutil.which to return None
    mocker.patch('shutil.which').return_value = None

    # set sys.exit mock to return an exception
    sys_exit_mock.side_effect = [Exception()]

    # call main
    with pytest.raises(Exception):
        pooetry.main()

    # assert sys.exit was called with error about poetry not found
    sys_exit_mock.assert_called_once()
    args, _ = sys_exit_mock.call_args
    msg = args[0]
    assert "poetry" in msg and "not found" in msg


def test_run_patch__should_pass_fixed_index_url_to_poetry__when_index_url_is_valid(poetry_mock, unpatched_run_mock):
    # valid url with creds that need to be urlencoded
    url_unencoded = 'https://user@example.com:p@$$w0rd@example.com'

    # same url except the creds have been urlencoded
    url_encoded = 'https://user%40example.com:p%40%24%24w0rd@example.com'

    # valid args with unencoded index-url
    valid_args = ['--index-url', url_unencoded]

    # call run_patch
    pooetry.run_patch(
        poetry_mock.installation.pip_installer.PipInstaller, *valid_args)

    # assert poetry was called with fixed index-url
    unpatched_run_mock.assert_called_once()
    args, _ = unpatched_run_mock.call_args
    assert args[1] == url_encoded


def test_run_patch__should_not_modify_pip_args__when_index_url_is_not_present(poetry_mock, unpatched_run_mock):
    # valid args without index-url
    valid_args = ['install']

    # call run_patch
    pooetry.run_patch(
        poetry_mock.installation.pip_installer.PipInstaller, *valid_args)

    # assert poetry was called and args were not modified
    unpatched_run_mock.assert_called_once()
    args, _ = unpatched_run_mock.call_args

    assert args[0] == valid_args[0] and len(args) == 1


def test_run_patch__should_return_error__when_fix_creds_raises_an_exception(mocker, poetry_mock, sys_exit_mock):
    # mock fix_creds and set side-effect of fix_creds mock to an exception
    mock_msg = 'test exception'
    mocker.patch('pooetry.main.fix_creds').side_effect = ValueError(mock_msg)

    # valid args without index-url
    valid_args = ['--index-url', 'https://example.com']

    # call run_patch
    pooetry.run_patch(
        poetry_mock.installation.pip_installer.PipInstaller, *valid_args)

    # assert sys.exit was called with error from fix_creds exception
    sys_exit_mock.assert_called_once()
    args, _ = sys_exit_mock.call_args
    msg = args[0]
    assert "credentials" in msg and mock_msg in msg


def test_fix_creds__should_urlencode_creds_in_url__when_url_is_valid():
    # valid url with creds that need to be urlencoded
    url_unencoded = 'https://user@example.com:p@$$w0rd@example.com'

    # same url except the creds have been urlencoded
    url_encoded = 'https://user%40example.com:p%40%24%24w0rd@example.com'

    # call fix_creds
    fixed_url = pooetry.fix_creds(url_unencoded)

    # assert fix_creds returned url with fixed creds
    assert fixed_url == url_encoded


def test_fix_creds__should_not_modify_url__when_creds_are_already_quoted():
    # valid url with creds that are pre-encoded
    url_encoded = 'https://user%40example.com:p%40%24%24w0rd@example.com'

    # call fix_creds
    fixed_url = pooetry.fix_creds(url_encoded)

    # assert fix_creds returned same url
    assert fixed_url == url_encoded


def test_fix_creds__should_not_modify_url__when_url_does_not_contain_creds():
    # valid url with no creds
    url = 'https://example.com'

    # call fix_creds
    fixed_url = pooetry.fix_creds(url)

    # assert fix_creds returned same url
    assert fixed_url == url
