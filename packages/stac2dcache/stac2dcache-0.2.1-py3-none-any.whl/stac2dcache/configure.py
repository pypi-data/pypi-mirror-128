import stac2dcache

from .filesystem import configure_filesystem
from .stac_io import configure_stac_io


def configure(username=None, password=None, token_filename=None):
    """
    Configure authentication to dCache with either username/passwd or token.

    :param username: (optional, str)
    :param password: (optional, str)
    :param token_filename: (optional, str) path to file with the token
    """
    stac2dcache.fs = configure_filesystem(
        filesystem="dcache",
        username=username,
        password=password,
        token_filename=token_filename,
    )
    stac2dcache.stac_io = configure_stac_io(stac2dcache.fs)
