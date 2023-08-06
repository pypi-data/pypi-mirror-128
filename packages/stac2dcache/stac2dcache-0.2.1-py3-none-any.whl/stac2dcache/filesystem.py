import aiohttp
import configparser
import dcachefs
import fsspec
import os
import pathlib

from fsspec.core import split_protocol

fsspec.register_implementation("dcache", dcachefs.dCacheFileSystem)

CHUNKSIZE = 5 * 2**20  # default chunk size for streaming


def configure_filesystem(filesystem="https", username=None, password=None,
                         token_filename=None):
    """
    Configure a http-based filesystem with authentication credentials.

    :param filesystem: (str)
    :param username: (optional, str)
    :param password: (optional, str)
    :param token_filename: (optional, str) path to file with the token
    """
    client_kwargs = {}
    # use username/password authentication
    if (username is None) ^ (password is None):
        raise ValueError("Username or password not provided")
    if (username is not None) and (password is not None):
        client_kwargs.update(auth=aiohttp.BasicAuth(username, password))

    # use bearer token authentication
    token = _get_token(token_filename)
    if token is not None:
        if password is not None:
            raise ValueError("Provide either token or username/password")
        client_kwargs.update(headers=dict(Authorization=f"Bearer {token}"))

    # get fsspec filesystem
    filesystem_class = fsspec.get_filesystem_class(filesystem)
    filesystem = filesystem_class(
        client_kwargs=client_kwargs,
        block_size=0,  # stream mode
    )
    return filesystem


def copy(source, dest, filesystem_from=None, filesystem_to=None):
    """
    Copy a file from the source to the destination file system

    :param source: (str) urlpath of the file to copy
    :param dest: (str) urlpath of the folder where to save the file
    :param filesystem_from: (`fsspec` compatible file system instance)
    :param filesystem_to: (`fsspec` compatible file system instance.)
    :return (str) urlpath of the copied file
    """
    _, filename = os.path.split(source)
    target = os.path.join(dest, filename)

    filesystem_from = filesystem_from or \
        fsspec.filesystem(split_protocol(source)[0])
    filesystem_to = filesystem_to or \
        fsspec.filesystem(split_protocol(dest)[0])

    with filesystem_from.open(source, "rb") as f_read:
        filesystem_to.makedirs(dest, exist_ok=True)
        with filesystem_to.open(target, "wb") as f_write:
            if isinstance(filesystem_to, dcachefs.dCacheFileSystem):
                f_write.write(f_read)  # stream upload of file-like object
            else:
                data = True
                while data:
                    data = f_read.read(CHUNKSIZE)
                    f_write.write(data)

    return target


def _get_token(filename=None):
    """
    Read the token from a file

    :param filename: (optional, str) name of the file
    """
    token = None
    if filename is not None:
        filepath = pathlib.Path(filename)
        assert filepath.exists(), f'Token file {filepath.as_posix()} not found'
        if filepath.suffix == '.conf':
            token = _parse_rclone_config_file(filepath)
        else:
            token = _parse_plain_file(filepath)
    return token


def _parse_rclone_config_file(filename):
    filepath = pathlib.Path(filename)
    config = configparser.ConfigParser()
    config.read(filepath)
    return config[filepath.stem]['bearer_token']


def _parse_plain_file(filename):
    filepath = pathlib.Path(filename)
    with filepath.open() as f:
        return f.read().strip()
