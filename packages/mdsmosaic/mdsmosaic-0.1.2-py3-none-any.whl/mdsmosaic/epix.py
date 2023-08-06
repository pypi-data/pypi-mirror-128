import functools
from typing import List, Any
from urllib.parse import urljoin

import zeep.helpers
from zeep import Client
from zeep.xsd import ComplexType

from .helpers import modify_url_for_urljoin
from .model import Identity
from .schema import load_identity, dump_identity


def create_epix_client(base_url: str) -> Client:
    """
    Creates a Zeep client for the E-PIX SOAP interface hosted at the given URL.

    :param base_url: URL where the E-PIX service is hosted
    :return: Zeep client
    """
    wsdl_url = urljoin(modify_url_for_urljoin(base_url), "epixService?wsdl")
    return Client(wsdl_url)


def get_mpi_request_type(client: Client) -> ComplexType:
    """
    Returns the MPI request type as defined by the SOAP interface.

    :param client: Zeep client with E-PIX SOAP methods
    :return: SOAP MPI request type
    """
    return client.get_type("ns0:mpiRequestDTO")


def _get_mpi_from_mpi_batch_response_entry(entry: Any) -> str:
    return entry.value.person.mpiId.value


def request_mpi_batch(client: Client, domain: str, source: str, identities: List[Identity]) -> List[str]:
    """
    Submits many identities to the MPI for creation. Returns the identifiers assigned to these identities.

    :param client: Zeep client with E-PIX SOAP methods
    :param domain: Data domain
    :param source: Data source
    :param identities: Identities to insert
    :return: List of identifiers
    """
    create_soap_mpi_batch_request = get_mpi_request_type(client)

    entries = [
        dump_identity(i) for i in identities
    ]

    request = create_soap_mpi_batch_request(
        domainName=domain,
        sourceName=source,
        requestEntries=entries
    )

    response = client.service.requestMPIBatch(request)

    if response is None:
        return []

    return [
        _get_mpi_from_mpi_batch_response_entry(e) for e in response.entry
    ]


def _get_identity_id_from_person_for_domain_response_entry(entry: Any) -> int:
    """
    Returns the MPI ID for an identity in a domain response entry.

    :param entry: Entry to extract MPI ID from
    :return: MPI ID
    """
    return entry.referenceIdentity.identityId


def get_identity_ids_in_domain(client: Client, domain: str) -> List[int]:
    """
    Fetches all identity IDs present in the given domain.

    :param client: Zeep client with E-PIX SOAP methods
    :param domain: Data domain
    :return: List of identity IDs
    """
    response = client.service.getPersonsForDomain(domain)
    return [
        _get_identity_id_from_person_for_domain_response_entry(e) for e in response
    ]


def delete_identity(client: Client, identity_id: int) -> None:
    """
    Deletes the identity with the given ID.

    :param client: Zeep client with E-PIX SOAP methods
    :param identity_id: ID of the identity to delete
    """
    client.service.deleteIdentity(identity_id)


def deactivate_identity(client: Client, identity_id: int) -> None:
    """
    Deactivates the identity with the given ID.

    :param client: Zeep client with E-PIX SOAP methods
    :param identity_id: ID of the identity to deactivate
    """
    client.service.deactivateIdentity(identity_id)


def resolve_person_for_mpi(client: Client, domain: str, mpi: str) -> Identity:
    """
    Looks up an identifier in the MPI and returns the corresponding personal entry, if present.

    :param client: Zeep client with E-PIX SOAP methods
    :param domain: Data domain
    :param mpi: MPI record identifier
    :return: Personal data associated with the given identifier
    """
    person_data = client.service.getPersonByMPI(domain, mpi)
    person_data_id = person_data["referenceIdentity"]

    return load_identity(zeep.helpers.serialize_object(person_data_id, dict))


class EPIXClient:

    def __init__(self, base_url: str):
        """
        Creates a convenience wrapper around selected E-PIX SOAP functions.

        :param base_url: URL where the E-PIX service is hosted
        """
        client = create_epix_client(base_url)
        self.resolve_person_for_mpi = functools.partial(resolve_person_for_mpi, client)
        self.request_mpi_batch = functools.partial(request_mpi_batch, client)
        self.get_mpis_in_domain = functools.partial(get_identity_ids_in_domain, client)
        self.delete_identity = functools.partial(delete_identity, client)
        self.deactivate_identity = functools.partial(deactivate_identity, client)
