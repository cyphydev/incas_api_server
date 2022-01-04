import connexion
import six

from uiuc_incas_server.models.message_enrichment import MessageEnrichment  # noqa: E501
from uiuc_incas_server.models.message_enrichment_meta import MessageEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server import util


def message_enrichments_delete(enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """message_enrichments_delete

    Delete specific message enrichment meta by providerName, enrichmentName and version # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def message_enrichments_get(enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """message_enrichments_get

    Returns current message enrichment meta by providerName, enrichmentName and version # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: MessageEnrichmentMeta
    """
    return 'do some magic!'


def message_enrichments_post(body):  # noqa: E501
    """message_enrichments_post

    Creates message enrichment meta (post after all messages have been added) # noqa: E501

    :param body: The new enrichment meta to add
    :type body: list | bytes

    :rtype: MessageEnrichmentMeta
    """
    if connexion.request.is_json:
        body = [MessageEnrichmentMeta.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def message_enrichments_put(body, enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """message_enrichments_put

    Updates message enrichment meta (after all messages have been added) by providerName, enrichmentName and version # noqa: E501

    :param body: The new enrichment meta to update
    :type body: list | bytes
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: MessageEnrichmentMeta
    """
    if connexion.request.is_json:
        body = [MessageEnrichmentMeta.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def message_id_enrichments_delete(id, enrichment_name, provider_name, version):  # noqa: E501
    """message_id_enrichments_delete

    Delete the enrichments for specific message by type, providerName and version # noqa: E501

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


def message_id_enrichments_get(id, enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """message_id_enrichments_get

    Returns all visible matched enrichment for the specific message by type, providerName and version # noqa: E501

    :param id: Message ID
    :type id: str
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: List[MessageEnrichment]
    """
    return 'do some magic!'


def message_id_enrichments_post(body, id):  # noqa: E501
    """message_id_enrichments_post

    Creates new enrichments for specific message # noqa: E501

    :param body: The new enrichment to add
    :type body: list | bytes
    :param id: Message ID
    :type id: str

    :rtype: List[MessageEnrichment]
    """
    if connexion.request.is_json:
        body = [MessageEnrichment.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def message_id_enrichments_put(body, enrichment_name, provider_name, version, id):  # noqa: E501
    """message_id_enrichments_put

    Update the enrichments for specific message by type, providerName and version # noqa: E501

    :param body: The new enrichments to update
    :type body: list | bytes
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str
    :param id: Message ID
    :type id: str

    :rtype: List[MessageEnrichment]
    """
    if connexion.request.is_json:
        body = [MessageEnrichment.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def message_id_get(id):  # noqa: E501
    """message_id_get

    Returns specific message by id # noqa: E501

    :param id: Message ID
    :type id: str

    :rtype: UiucMessage
    """
    return 'do some magic!'
