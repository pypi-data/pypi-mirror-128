# -*- coding: utf-8 -*-

"""Download functionality for UMLS."""

import logging
from pathlib import Path
from typing import Optional, Union

import bs4
import pystow
import pystow.utils
import requests

__all__ = [
    "download_tgt",
    "download_umls",
]

logger = logging.getLogger(__name__)

MODULE = pystow.module("bio", "umls")
TGT_URL = "https://utslogin.nlm.nih.gov/cas/v1/api-key"


def download_tgt(url: str, path: Union[str, Path], *, api_key: Optional[str] = None) -> None:
    """Download a file via the UMLS ticket granting system.

    This implementation is based on the instructions listed at
    https://documentation.uts.nlm.nih.gov/automating-downloads.html.

    :param url: The URL of the file to download, like
        ``https://download.nlm.nih.gov/umls/kss/2021AB/umls-2021AB-mrconso.zip``
    :param path: The local file path where the file should be downloaded
    :param api_key: An API key. If not given, looks up using :func:`pystow.get_config`
        with the ``umls`` module and ``api_key`` key.
    """
    if api_key is None:
        api_key = pystow.get_config("umls", "api_key", raise_on_missing=True)

    # Step 1: get a link to the ticket granting system (TGT)
    auth_res = requests.post(TGT_URL, data={"apikey": api_key})
    #  for some reason, this API returns HTML. This needs to be parsed,
    #  and there will be a form whose action is the next thing to POST to
    soup = bs4.BeautifulSoup(auth_res.text, features="html.parser")
    action_url = soup.find("form").attrs["action"]
    logger.info("[umls] got TGT url: %s", action_url)

    # Step 2: get a service ticket for the file you want to download
    #  by POSTing to the action URL with the name of the URL you actually
    #  want to download inside the form data
    key_res = requests.post(action_url, data={"service": url})
    # luckily this one just returns the text you need
    service_ticket = key_res.text
    logger.info("[umls] got service ticket: %s", service_ticket)

    # Step 3: actually try downloading the file you want, using the
    # service ticket issued in the last step as a query parameter
    pystow.utils.download(
        url=url,
        path=path,
        backend="requests",
        params={"ticket": service_ticket},
    )


def download_umls(version: Optional[str] = None, *, api_key: Optional[str] = None) -> Path:
    """Ensure the given version of the UMLS MRCONSO.RRF file."""
    if version is None:
        import bioversions

        version = bioversions.get_version("umls")
    url = f"https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-mrconso.zip"
    path = MODULE.join(version, name=f"umls-{version}-mrconso.zip")
    download_tgt(url, path, api_key=api_key)
    return path
