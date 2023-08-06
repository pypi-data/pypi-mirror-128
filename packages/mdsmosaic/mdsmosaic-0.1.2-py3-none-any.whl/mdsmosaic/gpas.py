import functools
from typing import List, Dict
from urllib.parse import urljoin

from zeep import Client

from .helpers import modify_url_for_urljoin


def create_gpas_client(base_url: str) -> Client:
    """
    Creates a Zeep client for the gPAS SOAP interface hosted at the given URL.

    :param base_url: URL where the gPAS service is hosted
    :return: Zeep client
    """
    wsdl_url = urljoin(modify_url_for_urljoin(base_url), "gpasService?wsdl")
    return Client(wsdl_url)


def resolve_pseudonym(client: Client, domain: str, pseudonym: str) -> str:
    """
    Looks up a domain-specific pseudonym and returns the corresponding identifier that is associated with it.

    :param client: Zeep client with gPAS SOAP methods
    :param domain: Data domain
    :param pseudonym: Psudonym to resolve
    :return: Identifier that is associated with the given pseudonym
    """
    return client.service.getValueFor(pseudonym, domain)


def get_or_create_pseudonyms(client: Client, domain: str, values: List[str]) -> Dict[str, str]:
    """
    Gets or creates pseudonyms for the given values in the provided domain.

    :param client: Zeep client with gPAS SOAP methods
    :param domain: Data domain
    :param values: Values to create pseudonyms for
    :return: Mapping of values to their pseudonyms
    """
    resp = client.service.getOrCreatePseudonymForList(values, domain)

    return {
        entry.key: entry.value for entry in resp
    }


def delete_entries(client: Client, domain: str, values: List[str]) -> bool:
    """
    Deletes entries from the database. These are not pseudonyms but rather the values that were used to
    create the pseudonyms.

    :param client: Zeep client with gPAS SOAP methods
    :param domain: Data domain
    :param values: Values to delete
    :return: ``True`` if all values have been deleted successfully, ``False`` otherwise
    """
    if len(values) == 0:
        return True

    resp = client.service.deleteEntries(values, domain)

    for entry in resp:
        if entry.value != "SUCCESS":
            return False

    return True


class GPASClient:

    def __init__(self, base_url: str):
        """
        Creates a convenience wrapper around selected gPAS SOAP functions.

        :param base_url: URL where the gPAS service is hosted
        """
        client = create_gpas_client(base_url)
        self.resolve_pseudonym = functools.partial(resolve_pseudonym, client)
        self.get_or_create_pseudonyms = functools.partial(get_or_create_pseudonyms, client)
        self.delete_entries = functools.partial(delete_entries, client)
