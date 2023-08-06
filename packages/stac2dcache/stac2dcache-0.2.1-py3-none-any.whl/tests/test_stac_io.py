import fsspec
import pystac

from stac2dcache.stac_io import configure_stac_io, CustomIO

from . import test_data_path


def test_configure_stac_io_():
    fs = fsspec.filesystem("file")
    catalog_path = (test_data_path/"s2-catalog/catalog.json").as_posix()
    stac_io = configure_stac_io(filesystem=fs)
    catalog = pystac.Catalog.from_file(catalog_path, stac_io=stac_io)
    assert isinstance(catalog._stac_io, CustomIO)
    assert hasattr(catalog._stac_io, "filesystem")
    assert isinstance(
        catalog._stac_io.filesystem,
        fsspec.get_filesystem_class("file")
    )
