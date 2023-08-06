from pystac.stac_io import DefaultStacIO


class CustomIO(DefaultStacIO):
    """
    Object to perform IO tasks with a `fsspec` compatible file system.

    :param filesystem: `fsspec` compatible file system instance.
    """
    def __init__(self, filesystem):
        self.filesystem = filesystem

    def read_text_from_href(self, href):
        """
        Read from local or remote file system.

        :param href: (str) URI where to read from.
        """
        if self.filesystem is not None:
            with self.filesystem.open(href, mode="r") as f:
                text = f.read()
        else:
            text = super().read_text_from_href(href)
        return text

    def write_text_to_href(self, href, txt):
        """
        Write to local or remote file system.

        :param href: (str) URI where to write to.
        :param txt: (str) text to be written.
        """
        if self.filesystem is not None:
            with self.filesystem.open(href, mode="w") as f:
                f.write(txt)
        else:
            super().write_text_to_href(href=href, txt=txt)


def configure_stac_io(filesystem=None):
    """
    Configure PySTAC to read from/write to the provided file system.

    :param filesystem: `fsspec` compatible file system instance.
    """
    return CustomIO(filesystem)
