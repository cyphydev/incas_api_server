import connexion
import six

from uiuc_incas_server.models.enrichments_batch_delete_body import EnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_get_body import EnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_batch_get_body import MessageBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_enrichment import MessageEnrichment  # noqa: E501
from uiuc_incas_server.models.message_enrichment_meta import MessageEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server import util


def message_batch_get(body):  # noqa: E501
    """message_batch_get

    Returns a batch of messages given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: List[UiucMessage]
    """
    if connexion.request.is_json:
        body = MessageBatchGetBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_count_get():  # noqa: E501
    """message_count_get

    Return the number of message IDs available. # noqa: E501


    :rtype: int
    """
    return 'do some magic!'


def message_enrichments_batch_delete(body):  # noqa: E501
    """message_enrichments_batch_delete

    Deletes a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = EnrichmentsBatchDeleteBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_enrichments_batch_get(body):  # noqa: E501
    """message_enrichments_batch_get

    Returns a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: Dict[str, List[MessageEnrichment]]
    """
    if connexion.request.is_json:
        body = EnrichmentsBatchGetBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_enrichments_batch_post(body):  # noqa: E501
    """message_enrichments_batch_post

    Submits a enrichment for each message ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Dict[str, MessageEnrichment].from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_enrichments_batch_put(body):  # noqa: E501
    """message_enrichments_batch_put

    Updates a enrichment for each message ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Dict[str, MessageEnrichment].from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_enrichments_meta_delete(enrichment_name, provider_name, version):  # noqa: E501
    """message_enrichments_meta_delete

    Delete specific message enrichment meta by providerName, enrichmentName and version. # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def message_enrichments_meta_get(enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """message_enrichments_meta_get

    Returns current message enrichment metas by providerName, enrichmentName and version. # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: List[MessageEnrichmentMeta]
    """
    return 'do some magic!'


def message_enrichments_meta_post(body):  # noqa: E501
    """message_enrichments_meta_post

    Submits a message enrichment meta (post after all messages have been added). # noqa: E501

    :param body: The new enrichment meta to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = MessageEnrichmentMeta.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_enrichments_meta_put(body):  # noqa: E501
    """message_enrichments_meta_put

    Updates message enrichment meta (after all messages have been added) by providerName, enrichmentName and version. # noqa: E501

    :param body: The new enrichment meta to update
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = MessageEnrichmentMeta.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_id_enrichments_delete(id, enrichment_name, provider_name, version):  # noqa: E501
    """message_id_enrichments_delete

    Delete a enrichment for specific message by type, providerName and version. # noqa: E501

    :param id: Message ID
    :type id: str
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def message_id_enrichments_get(id, enrichment_name=None, provider_name=None, version=None, dev=None):  # noqa: E501
    """message_id_enrichments_get

    Returns all visible matched enrichment for the specific message by type, providerName and version. # noqa: E501

    :param id: Message ID
    :type id: str
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str
    :param dev: 
    :type dev: bool

    :rtype: List[MessageEnrichment]
    """
    return 'do some magic!'


def message_id_enrichments_post(body, id):  # noqa: E501
    """message_id_enrichments_post

    Submits a new enrichment for specific message. # noqa: E501

    :param body: The new enrichment to add
    :type body: dict | bytes
    :param id: Message ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = MessageEnrichment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_id_enrichments_put(body, id):  # noqa: E501
    """message_id_enrichments_put

    Update a enrichment for specific message by type, providerName and version. # noqa: E501

    :param body: The new enrichments to update
    :type body: dict | bytes
    :param id: Message ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = MessageEnrichment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_id_get(id, with_enrichment=None, enrichment_name=None, provider_name=None, version=None, dev=None):  # noqa: E501
    """message_id_get

    Returns specific message by id. # noqa: E501

    :param id: Message ID
    :type id: str
    :param with_enrichment: Whether to retrieve enrichments
    :type with_enrichment: bool
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str
    :param dev: 
    :type dev: bool

    :rtype: UiucMessage
    """
    return 'do some magic!'


def message_list_get(begin, end):  # noqa: E501
    """message_list_get

    Return list of message IDs available in [begin, end). # noqa: E501

    :param begin: Begin
    :type begin: int
    :param end: End
    :type end: int

    :rtype: List[str]
    """
    return 'do some magic!'
