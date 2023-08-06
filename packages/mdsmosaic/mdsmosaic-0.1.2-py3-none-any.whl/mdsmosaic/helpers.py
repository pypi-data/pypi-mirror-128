import urllib.parse


def modify_url_for_urljoin(url: str):
    """
    Removes params, query and fragment from the URL and adds a trailing slash to the path if it doesn't exist yet.

    :param url: URL to modify
    :return: Modified URL
    """
    scheme, host, path, _, _, _ = urllib.parse.urlparse(url)

    if not host.endswith("/"):
        host = host + "/"

    return urllib.parse.urlunparse((scheme, host, path, "", "", ""))
