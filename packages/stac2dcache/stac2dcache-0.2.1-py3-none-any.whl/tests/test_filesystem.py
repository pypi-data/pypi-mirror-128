import fsspec
import pytest

from stac2dcache.filesystem import configure_filesystem

from . import test_data_path


def test_configure_filesystem_returns_correct_fs_class():
    for fs_type in ("http", "dcache", "file"):
        fs_class = fsspec.get_filesystem_class(fs_type)
        fs = configure_filesystem(filesystem=fs_type)
        assert isinstance(fs, fs_class)


def test_configure_filesystem_sets_username_and_password():
    auth = dict(username="user", password="pass")
    for fs_type in ("http", "dcache"):
        fs = configure_filesystem(filesystem=fs_type,
                                  **auth)
        assert fs.client_kwargs['auth'].login == auth["username"]
        assert fs.client_kwargs['auth'].password == auth["password"]


def test_configure_filesystem_sets_token_filename():
    # test two formats for the token file
    for token_file in (test_data_path/"macaroon.conf",
                       test_data_path/"macaroon.dat"):
        for fs_type in ("http", "dcache"):
            fs = configure_filesystem(filesystem=fs_type,
                                      token_filename=token_file)
            assert "Authorization" in fs.client_kwargs["headers"]


def test_configure_filesystem_checks_authentication_methods():
    with pytest.raises(ValueError):
        configure_filesystem(username="user")  # missing password
    with pytest.raises(ValueError):
        configure_filesystem(username="user")  # missing username
    with pytest.raises(ValueError):
        configure_filesystem(token_filename=test_data_path/"macaroon.conf",
                             username="user",
                             password="passwd")  # uname/passwd and token
