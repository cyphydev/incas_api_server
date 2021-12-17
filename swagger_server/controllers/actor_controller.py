import connexion
import six

from swagger_server.models.actor import Actor  # noqa: E501
from swagger_server.models.actor_enrichment import ActorEnrichment  # noqa: E501
from swagger_server.models.actor_enrichment_meta import ActorEnrichmentMeta  # noqa: E501
from swagger_server import util


def actor_enrichments_delete(enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """actor_enrichments_delete

    Delete specific actor enrichment meta by providerName, enrichmentName and version # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def actor_enrichments_get(enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """actor_enrichments_get

    Returns current actor enrichment meta by providerName, enrichmentName and version # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: ActorEnrichmentMeta
    """
    return 'do some magic!'


def actor_enrichments_post(body):  # noqa: E501
    """actor_enrichments_post

    Creates actor enrichment meta (post after all actors have been added) # noqa: E501

    :param body: The new enrichment meta to add
    :type body: list | bytes

    :rtype: ActorEnrichmentMeta
    """
    if connexion.request.is_json:
        body = [ActorEnrichmentMeta.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def actor_enrichments_put(body, enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """actor_enrichments_put

    Updates actor enrichment meta (after all actors have been added) by providerName, enrichmentName and version # noqa: E501

    :param body: The new enrichment meta to update
    :type body: list | bytes
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: ActorEnrichmentMeta
    """
    if connexion.request.is_json:
        body = [ActorEnrichmentMeta.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def actor_id_enrichments_delete(id, enrichment_name, provider_name, version):  # noqa: E501
    """actor_id_enrichments_delete

    Delete the enrichments for specific actor by type, providerName and version # noqa: E501

    :param id: Actor ID
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


def actor_id_enrichments_get(id, enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """actor_id_enrichments_get

    Returns all matched enrichment for the specific actor by type, providerName and version # noqa: E501

    :param id: Actor ID
    :type id: str
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: List[ActorEnrichment]
    """
    return 'do some magic!'


def actor_id_enrichments_post(body, id):  # noqa: E501
    """actor_id_enrichments_post

    Creates new enrichments for specific message # noqa: E501

    :param body: The new enrichment to add
    :type body: list | bytes
    :param id: Actor ID
    :type id: str

    :rtype: List[ActorEnrichment]
    """
    if connexion.request.is_json:
        body = [ActorEnrichment.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def actor_id_enrichments_put(body, enrichment_name, provider_name, version, id):  # noqa: E501
    """actor_id_enrichments_put

    Update the enrichments for specific actor by type, providerName and version # noqa: E501

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

    :rtype: List[ActorEnrichment]
    """
    if connexion.request.is_json:
        body = [ActorEnrichment.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def actor_id_get(id):  # noqa: E501
    """actor_id_get

    Returns specific actor by id # noqa: E501

    :param id: Actor ID
    :type id: str

    :rtype: Actor
    """
    return 'do some magic!'
