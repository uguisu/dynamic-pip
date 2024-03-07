# coding=utf-8
# author xin.he
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit


def download_file(
        url: str,
        filename: str = None,
        directory: str = None,
        is_overwrite: bool = False
):
    """
    download file
    """
    filename = filename or urlsplit(url).path.split('/')[-1]
    filename = Path(filename)
    # verify
    if len(filename.parts) > 1:
        raise ValueError('The `filename` contains a path, please delete the path and try again.')

    # create the directory if it does not exist, then update `filename`
    if directory is not None:
        directory = Path(directory)
        directory.mkdir(
            parents=True,
            exist_ok=True
        )
        filename = directory / filename

    if not filename.exists() or is_overwrite:
        # start download
        urllib.request.urlretrieve(
            url=url,
            filename=filename
        )
