import connexion
import six

import redis
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.actor_batch_get_body import ActorBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichment import ActorEnrichment  # noqa: E501
from uiuc_incas_server.models.actor_enrichment_meta import ActorEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_delete_body1 import EnrichmentsBatchDeleteBody1  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_get_body1 import EnrichmentsBatchGetBody1  # noqa: E501
from uiuc_incas_server.models.uiuc_actor import UiucActor  # noqa: E501
from uiuc_incas_server import util

get_db = connexion.utils.get_function_from_name('uiuc_incas_server.util.get_db')


def actor_batch_get(body):  # noqa: E501
    """actor_batch_get

    Returns a batch of actors given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: List[UiucActor]
    """
    if connexion.request.is_json:
        body = ActorBatchGetBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_count_get():  # noqa: E501
    """actor_count_get

    Return the number of actor IDs available. # noqa: E501


    :rtype: int
    """
    return 'do some magic!'


def actor_enrichments_batch_delete(body):  # noqa: E501
    """actor_enrichments_batch_delete

    Deletes a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = EnrichmentsBatchDeleteBody1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_enrichments_batch_get(body):  # noqa: E501
    """actor_enrichments_batch_get

    Returns a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: Dict[str, List[ActorEnrichment]]
    """
    if connexion.request.is_json:
        body = EnrichmentsBatchGetBody1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_enrichments_batch_post(body):  # noqa: E501
    """actor_enrichments_batch_post

    Submits a enrichment for each actor ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Dict[str, ActorEnrichment].from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_enrichments_batch_put(body):  # noqa: E501
    """actor_enrichments_batch_put

    Updates a enrichment for each actor ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Dict[str, ActorEnrichment].from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_enrichments_meta_delete(enrichment_name, provider_name, version):  # noqa: E501
    """actor_enrichments_meta_delete

    Delete a specific message enrichment meta by providerName, enrichmentName and version. # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def actor_enrichments_meta_get(enrichment_name=None, provider_name=None, version=None):  # noqa: E501
    """actor_enrichments_meta_get

    Returns current actor enrichment metas by providerName, enrichmentName and version. # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: List[ActorEnrichmentMeta]
    """
    return 'do some magic!'


def actor_enrichments_meta_post(body):  # noqa: E501
    """actor_enrichments_meta_post

    Submits an actor enrichment meta (post after all actors have been added). # noqa: E501

    :param body: The new enrichment meta to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ActorEnrichmentMeta.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_enrichments_meta_put(body):  # noqa: E501
    """actor_enrichments_meta_put

    Updates an actor enrichment meta (after all actors have been added) by providerName, enrichmentName and version. # noqa: E501

    :param body: The new enrichment meta to update
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ActorEnrichmentMeta.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_id_enrichments_delete(id_, enrichment_name, provider_name, version):  # noqa: E501
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


def actor_id_enrichments_get(id_, enrichment_name=None, provider_name=None, version=None, dev=None):  # noqa: E501
    """actor_id_enrichments_get

    Returns all matched enrichment for the specific actor by type, providerName and version. # noqa: E501

    :param id: Actor ID
    :type id: str
    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str
    :param dev: 
    :type dev: bool

    :rtype: List[ActorEnrichment]
    """
    return 'do some magic!'


def actor_id_enrichments_post(body, id_):  # noqa: E501
    """actor_id_enrichments_post

    Submits a new enrichment for specific message. # noqa: E501

    :param body: The new enrichment to add
    :type body: dict | bytes
    :param id: Actor ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = ActorEnrichment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_id_enrichments_put(body, id_):  # noqa: E501
    """actor_id_enrichments_put

    Update the enrichments for specific actor by type, providerName and version. # noqa: E501

    :param body: The new enrichments to update
    :type body: dict | bytes
    :param id: Actor ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = ActorEnrichment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_id_get(id_, with_enrichment=None, enrichment_name=None, provider_name=None, version=None, dev=None):  # noqa: E501
    """actor_id_get

    Returns specific actor by id. # noqa: E501

    :param id: Actor ID
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

    :rtype: UiucActor
    """
    return 'do some magic!'


def actor_list_get(begin, end):  # noqa: E501
    """actor_list_get

    Return list of actor IDs available in [begin, end). # noqa: E501

    :param begin: Begin
    :type begin: int
    :param end: End
    :type end: int

    :rtype: List[str]
    """
    return 'do some magic!'
