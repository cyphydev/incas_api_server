import connexion
import six
import dpath.util
from itertools import chain

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.actor_batch_get_body import ActorBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichment import ActorEnrichment  # noqa: E501
from uiuc_incas_server.models.actor_enrichment_meta import ActorEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_delete_body import ActorEnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_delete_validation_response import ActorEnrichmentsBatchDeleteValidationResponse  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_get_body import ActorEnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_validation_response import ActorEnrichmentsBatchValidationResponse  # noqa: E501
from uiuc_incas_server.models.actor_id_response import ActorIdResponse  # noqa: E501
from uiuc_incas_server.models.actor_segment_collection import ActorSegmentCollection  # noqa: E501
from uiuc_incas_server.models.actor_segments_batch_delete_body import ActorSegmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.actor_segments_batch_delete_validation_response import ActorSegmentsBatchDeleteValidationResponse  # noqa: E501
from uiuc_incas_server.models.actor_segments_batch_get_body import ActorSegmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_segments_batch_validation_response import ActorSegmentsBatchValidationResponse  # noqa: E501
from uiuc_incas_server.models.uiuc_actor import UiucActor  # noqa: E501
from uiuc_incas_server.models.uiuc_segment_collection import UiucSegmentCollection  # noqa: E501
from uiuc_incas_server import util

@util.generic_db_lock_decor
def actor_batch_get(body, user=None, token_info=None):  # noqa: E501
    """actor_batch_get

    Returns a batch of actors given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: List[UiucActor]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorBatchGetBody)  # noqa: E501
        enrichment_pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.enrichment_provider_name, body.enrichment_version)
        collection_pattern = util.get_collection_pattern('actor', body.collection_name, body.collection_provider_name, body.collection_version)

        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_enrichment_metas = util.get_all_keys(db_meta, enrichment_pattern)
            available_collection_metas = util.get_all_keys(db_meta, collection_pattern)

        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            records = db_data.json().mget(body.ids, Path.rootPath())
        
        for i in range(len(records)):
            if records[i] is None:
                continue
            if body.with_enrichment:
                if body.dev:
                    enrichments = records[i]['enrichments']
                else:
                    enrichments = {k: v for k, v in records[i]['enrichments'].items() if k in available_enrichment_metas}
                records[i]['enrichments'] = dpath.util.values(enrichments, enrichment_pattern)
            else:
                records[i]['enrichments'] = []
            if body.with_segment:
                if body.dev:
                    segments = records[i]['segmentCollections']
                else:
                    segments = {k: v for k, v in records[i]['segmentCollections'].items() if k in available_collection_metas}
                records[i]['segmentCollections'] = dpath.util.values(segments, collection_pattern)
            else:
                records[i]['segmentCollections'] = []
            records[i] = util.deserialize(records[i], UiucActor)

        return records, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_count_get(media_type, entity_type=None, user=None, token_info=None):  # noqa: E501
    """actor_count_get

    Return the number of actor IDs available. # noqa: E501

    :param media_type: Type of entity to retrieve
    :type media_type: str
    :param entity_type: Type of entity to retrieve
    :type entity_type: str

    :rtype: int
    """
    db_idx = util.get_db(db_name='index')
    if entity_type is None:
        entity_type = '*'
    with db_idx.lock('db_index_lock', blocking_timeout=5) as lock:
        cnt = util.count_keys(db_idx, f'forward:actor:{media_type.lower()}:{entity_type.lower()}*')
    return cnt, 200


@util.generic_db_lock_decor
def actor_enrichments_batch_delete(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_batch_delete

    Deletes a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentsBatchDeleteBody)  # noqa: E501
        pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if db_meta.exists(pattern):
                return 'Enrichment meta must be deleted first', 400

        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            for id_ in body.ids:
                if not db_data.exists(id_):
                    return f'ID {id_} not found, nothing is done', 404
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    return f'Enrichment {pattern} not found in {id_}, nothing is done', 404
            for id_ in body.ids:
                db_data.json().delete(id_, Path(f'enrichments["{pattern}"]'))
        return 'Deleted', 204
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_batch_delete_validate(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_batch_delete_validate

    Validation endpoint for batch enrichment deletion, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: ActorEnrichmentsBatchDeleteValidationResponse
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentsBatchDeleteBody)  # noqa: E501
        pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if db_meta.exists(pattern):
                return 'Enrichment meta must be deleted first', 400

        ret = ActorEnrichmentsBatchDeleteValidationResponse(id_invalid=[], value_not_found=[])
        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            for id_ in body.ids:
                if not db_data.exists(id_):
                    ret.id_invalid.append(id_)
                elif db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    ret.value_not_found.append(id_)
        return ret, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_batch_get(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_batch_get

    Returns a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: Dict[str, List[ActorEnrichment]]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentsBatchGetBody)  # noqa: E501
        pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)

        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_metas = util.get_all_keys(db_meta, pattern)

        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            all_enrichments = db_data.json().mget(body.ids, Path('enrichments'))

        for i in range(len(all_enrichments)):
            if all_enrichments[i] is None:
                continue
            enrichments = all_enrichments[i]
            if not body.dev:
                enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
            all_enrichments[i] = [util.deserialize(v, ActorEnrichment) for v in dpath.util.values(enrichments, pattern)]
        return all_enrichments, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_batch_post(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_batch_post

    Submits a enrichment for each actor ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if not db_data.exists(id_):
                    return f'ID {id_} does not exist, nothing is done', 404
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
                    return f'Enrichment {pattern} already exists in {id_}, nothing is done', 409
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
                db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Created', 201
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_batch_post_validate(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_batch_post_validate

    Validation endpoint for batch enrichment creation, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: ActorEnrichmentsBatchValidationResponse
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        seen_set = set()
        ret = ActorEnrichmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found=None, value_existed={})
        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    ret.value_invalid[id_] = body
                elif not db_data.exists(id_):
                    ret.id_invalid[id_] = body
                elif db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None or (id_, pattern) in seen_set:
                    ret.value_existed[id_] = body
                else:
                    seen_set.add((id_, pattern))
        return ret, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_batch_put(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_batch_put

    Updates a enrichment for each actor ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if not db_data.exists(id_):
                    return f'ID {id_} does not exist, nothing is done', 404
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    return f'Enrichment {pattern} not found in {id_}, nothing is done', 404
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
                db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Updated', 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_batch_put_validate(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_batch_put_validate

    Validation endpoint for batch enrichment update, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: ActorEnrichmentsBatchValidationResponse
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        ret = ActorEnrichmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found={}, value_existed=None)
        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    ret.value_invalid[id_] = body
                elif not db_data.exists(id_):
                    ret.id_invalid[id_] = body
                elif db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    ret.value_not_found[id_] = body
        return ret, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_meta_delete(enrichment_name, provider_name, version, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_meta_delete

    Delete a specific actor enrichment meta by providerName, enrichmentName and version. # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    pattern = util.get_enrichment_pattern('actor', enrichment_name, provider_name, version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        if not db_meta.exists(pattern):
            return 'Key not found', 404
        db_meta.json().delete(pattern, Path.rootPath())
    return 'Deleted', 204


@util.generic_db_lock_decor
def actor_enrichments_meta_get(enrichment_name=None, provider_name=None, version=None, user=None, token_info=None):  # noqa: E501
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
    pattern = util.get_enrichment_pattern('actor', enrichment_name, provider_name, version)

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        ks = util.get_all_keys(db_meta, pattern)
        if len(ks) == 0:
            return 'No keys found', 404
        
        records = db_meta.json().mget(ks, Path.rootPath())
        for i in range(len(records)):
            if records[i] is None:
                continue
            records[i] = util.deserialize(records[i], ActorEnrichmentMeta)
    return records, 200


@util.generic_db_lock_decor
def actor_enrichments_meta_post(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_meta_post

    Submits an actor enrichment meta (post after all actors have been added). # noqa: E501

    :param body: The new enrichment meta to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentMeta)  # noqa: E501
        pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if db_meta.exists(pattern):
                return 'Key already exists', 409
            db_meta.json().set(pattern, Path.rootPath(), util.serialize(body))
        return "Created", 201
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_enrichments_meta_put(body, user=None, token_info=None):  # noqa: E501
    """actor_enrichments_meta_put

    Updates an actor enrichment meta (after all actors have been added) by providerName, enrichmentName and version. # noqa: E501

    :param body: The new enrichment meta to update
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentMeta)  # noqa: E501
        pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if not db_meta.exists(pattern):
                return 'Key not found', 404
            db_meta.json().set(pattern, Path.rootPath(), util.serialize(body))
        return "Updated", 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_id_enrichments_delete(id_, enrichment_name, provider_name, version, user=None, token_info=None):  # noqa: E501
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
    pattern = util.get_enrichment_pattern('actor', enrichment_name, provider_name, version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        if db_meta.exists(pattern):
            return 'Enrichment meta must be deleted first', 400

    db_data = util.get_db(db_name='actor_data')
    with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
        if not db_data.exists(id_):
            return 'ID not found', 404
        if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
            return 'Enrichment not found', 404
        db_data.json().delete(id_, Path(f'enrichments["{pattern}"]'))
    return 'Deleted', 204


@util.generic_db_lock_decor
def actor_id_enrichments_get(id_, enrichment_name=None, provider_name=None, version=None, dev=None, user=None, token_info=None):  # noqa: E501
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
    pattern = util.get_enrichment_pattern('actor', enrichment_name, provider_name, version)

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        available_metas = util.get_all_keys(db_meta, pattern)

    db_data = util.get_db(db_name='actor_data')
    with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
        if not db_data.exists(id_):
            return 'ID does not exist', 404
        enrichments = db_data.json().get(id_, Path('enrichments'))
    
    if not dev:
        enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
    ret = [util.deserialize(v, ActorEnrichment) for v in dpath.util.values(enrichments, pattern)]
    return ret, 200


@util.generic_db_lock_decor
def actor_id_enrichments_post(body, id_, user=None, token_info=None):  # noqa: E501
    """actor_id_enrichments_post

    Submits a new enrichment for specific actor. # noqa: E501

    :param body: The new enrichment to add
    :type body: dict | bytes
    :param id: Actor ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichment)  # noqa: E501
        pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
                return 'Enrichment already exists', 409
            db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Created', 201
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_id_enrichments_put(body, id_, user=None, token_info=None):  # noqa: E501
    """actor_id_enrichments_put

    Update the enrichments for specific actor by type, providerName and version. # noqa: E501

    :param body: The new enrichments to update
    :type body: dict | bytes
    :param id: Actor ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichment)  # noqa: E501
        pattern = util.get_enrichment_pattern('actor', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                return 'Enrichment not found', 404
            db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Updated', 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_id_get(id_, with_enrichment=None, with_segment=None, enrichment_name=None, enrichment_provider_name=None, enrichment_version=None, collection_name=None, collection_provider_name=None, collection_version=None, dev=None, user=None, token_info=None):  # noqa: E501
    """actor_id_get

    Returns specific actor by id. # noqa: E501

    :param id: Actor ID
    :type id: str
    :param with_enrichment: Whether to retrieve enrichments
    :type with_enrichment: bool
    :param with_segment: Whether to retrieve segments
    :type with_segment: bool
    :param enrichment_name: 
    :type enrichment_name: str
    :param enrichment_provider_name: 
    :type enrichment_provider_name: str
    :param enrichment_version: 
    :type enrichment_version: str
    :param collection_name: 
    :type collection_name: str
    :param collection_provider_name: 
    :type collection_provider_name: str
    :param collection_version: 
    :type collection_version: str
    :param dev: 
    :type dev: bool

    :rtype: UiucActor
    """
    enrichment_pattern = util.get_enrichment_pattern('actor', enrichment_name, enrichment_provider_name, enrichment_version)
    collection_pattern = util.get_collection_pattern('actor', collection_name, collection_provider_name, collection_version)

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        available_enrichment_metas = util.get_all_keys(db_meta, enrichment_pattern)
        available_collection_metas = util.get_all_keys(db_meta, collection_pattern)

    db_data = util.get_db(db_name='actor_data')
    with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
        if not db_data.exists(id_):
            return 'Key does not exist', 404
        record = db_data.json().get(id_, Path.rootPath())
    
    if with_enrichment:
        if dev:
            enrichments = record['enrichments']
        else:
            enrichments = {k: v for k, v in record['enrichments'].items() if k in available_enrichment_metas}
        record['enrichments'] = dpath.util.values(enrichments, enrichment_pattern)
    else:
        record['enrichments'] = []
    
    if with_segment:
        segments = record['segmentCollections']
        record['segmentCollections'] = dpath.util.values(segments, collection_pattern)
    else:
        record['segmentCollections'] = []
        
    ret = util.deserialize(record, UiucActor)
    return ret, 200


@util.generic_db_lock_decor
def actor_id_segments_delete(id_, collection_name, provider_name, version, user=None, token_info=None):  # noqa: E501
    """actor_id_segments_delete

    Deletes all matched segments for specific actor by segmentCollectionName # noqa: E501

    :param id: Actor ID
    :type id: str
    :param collection_name: 
    :type collection_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    pattern = util.get_collection_pattern('actor', collection_name, provider_name, version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_data = util.get_db(db_name='actor_data')
    db_seg = util.get_db(db_name='segment')
    with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
        if not db_data.exists(id_):
            return 'ID not found', 404
        if db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is None:
            return 'Segment collection not found in the actor', 404
        # segments = db_data.json().get(id_, Path(f'segmentCollections["{pattern}"]'))
        
        with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
            if not db_seg.exists(pattern):
                return 'Segment collection not found, DB is inconsistent', 404
            db_data.json().delete(id_, Path(f'segmentCollections["{pattern}"]'))
            for segment in db_seg.json().objkeys(pattern, Path('segments')):
                if db_seg.json().type(pattern, Path(f'segments["{segment}"]["{id_}"]')) is not None:
                    db_seg.json().delete(pattern, Path(f'segments["{segment}"]["{id_}"]'))
    return 'Deleted', 204


@util.generic_db_lock_decor
def actor_id_segments_get(id_, collection_name=None, provider_name=None, version=None, dev=None, user=None, token_info=None):  # noqa: E501
    """actor_id_segments_get

    Returns all matched segment collections the actor belonged to by collectionName. # noqa: E501

    :param id: Actor ID
    :type id: str
    :param collection_name: 
    :type collection_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str
    :param dev: 
    :type dev: bool

    :rtype: List[ActorSegmentCollection]
    """
    pattern = util.get_collection_pattern('actor', collection_name, provider_name, version)

    db_data = util.get_db(db_name='actor_data')
    with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
        if not db_data.exists(id_):
            return 'ID does not exist', 404
        segcols = db_data.json().get(id_, Path('segmentCollections'))
    ret = [util.deserialize(v, ActorSegmentCollection) for v in dpath.util.values(segcols, pattern)]
    return ret, 200


@util.generic_db_lock_decor
def actor_id_segments_post(body, id_, user=None, token_info=None):  # noqa: E501
    """actor_id_segments_post

    Add a new segment collection for the specific actor # noqa: E501

    :param body: The new segment collections to add
    :type body: dict | bytes
    :param id: Actor ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorSegmentCollection)  # noqa: E501
        pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            if db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is not None:
                return 'Segment collection already exists', 409
            
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                if not db_seg.exists(pattern):
                    segcol = UiucSegmentCollection(
                        description='',
                        collection_name=body.collection_name,
                        provider_name=body.provider_name,
                        version=body.version,
                        segment_descriptions={k: '' for k in body.segments.keys()},
                        segments={k: {id_: v} for k, v in body.segments.items()})
                    db_seg.json().set(pattern, Path.rootPath(), util.serialize(segcol))
                else:
                    segs = db_seg.json().objkeys(pattern, Path('segments'))
                    # exist_flag = False
                    # for seg in segs:
                    #     if db_seg.json().type(pattern, Path(f'segments["{seg}"]["{id_}"]')) is not None:
                    #         exist_flag = True
                    #         break
                    # if exist_flag:
                    #     return 'Actor is already in this segment collection', 409
                    # for seg in segs:
                    #     if seg in body.segments:
                    #         db_seg.json().set(pattern, Path(f'segments["{seg}"]["{id_}"]'), body.segments[seg])
                    for seg in segs:
                        if db_seg.json().type(pattern, Path(f'segments["{seg}"]["{id_}"]')) is not None and seg not in body.segments:
                            db_seg.json().delete(pattern, Path(f'segments["{seg}"]["{id_}"]'))
                        elif seg in body.segments:
                            db_seg.json().set(pattern, Path(f'segments["{seg}"]["{id_}"]'), body.segments[seg])
                db_data.json().set(id_, Path(f'segmentCollections["{pattern}"]'), util.serialize(body))
        return 'Created', 201
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_id_segments_put(body, id_, user=None, token_info=None):  # noqa: E501
    """actor_id_segments_put

    Update a segment collection for the specific actor by segment name # noqa: E501

    :param body: The segment collections to update
    :type body: dict | bytes
    :param id: Actor ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorSegmentCollection)  # noqa: E501
        pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            if db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is None:
                return 'Segment collection does not exist', 404
            
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                if not db_seg.exists(pattern):
                    return 'Segment collection does not exist', 404
                else:
                    segs = db_seg.json().objkeys(pattern, Path('segments'))
                    # exist_flag = False
                    # for seg in segs:
                    #     if db_seg.json().type(pattern, Path(f'segments["{seg}"]["{id_}"]')) is not None:
                    #         exist_flag = True
                    #         break
                    # if not exist_flag:
                    #     return 'Actor does not appear to be in this segment collection', 404
                    for seg in segs:
                        if db_seg.json().type(pattern, Path(f'segments["{seg}"]["{id_}"]')) is not None and seg not in body.segments:
                            db_seg.json().delete(pattern, Path(f'segments["{seg}"]["{id_}"]'))
                        elif seg in body.segments:
                            db_seg.json().set(pattern, Path(f'segments["{seg}"]["{id_}"]'), body.segments[seg])
                db_data.json().set(id_, Path(f'segmentCollections["{pattern}"]'), util.serialize(body))
        return 'Updated', 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_list_get(begin, end, media_type, entity_type=None, user=None, token_info=None):  # noqa: E501
    """actor_list_get

    Return list of actor IDs available in [begin, end). # noqa: E501

    :param begin: Begin
    :type begin: int
    :param end: End
    :type end: int
    :param media_type: Type of entity to retrieve
    :type media_type: str
    :param entity_type: Type of entity to retrieve
    :type entity_type: str

    :rtype: List[ActorIdResponse]
    """
    if entity_type is None:
        entity_type = '*'
    
    db_idx = util.get_db(db_name='index')
    with db_idx.lock('db_index_lock', blocking_timeout=5) as lock:
        if entity_type != '*':
            keys = ['forward:actor:{}:{}:{}'.format(media_type.lower(), entity_type.lower(), i) for i in range(begin, end)]
        else:
            keys = chain(*[list(util.get_all_keys(db_idx, f'forward:actor:{media_type.lower()}:{entity_type.lower()}:{i}')) for i in range(begin, end)])
        ret = db_idx.json().mget(keys, Path.rootPath())
    ret = [util.deserialize(x, ActorIdResponse) for x in ret if x]
    return ret, 200


@util.generic_db_lock_decor
def actor_segment_batch_delete(body, user=None, token_info=None):  # noqa: E501
    """actor_segment_batch_delete

    Deletes a batch of segment collections given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorSegmentsBatchDeleteBody)  # noqa: E501
        pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
            
        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                if not db_seg.exists(pattern):
                    return f'Segment collection {pattern} not found, DB is inconsistent', 404

            for id_ in body.ids:
                if not db_data.exists(id_):
                    return f'ID {id_} not found, nothing is done', 404
                if db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is None:
                    return f'Segment collection {pattern} not found in {id_}, nothing is done', 404
            
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                for id_ in body.ids:
                    db_data.json().delete(id_, Path(f'segmentCollections["{pattern}"]'))
                    for segment in db_seg.json().objkeys(pattern, Path('segments')):
                        if db_seg.json().type(pattern, Path(f'segments["{segment}"]["{id_}"]')) is not None:
                            db_seg.json().delete(pattern, Path(f'segments["{segment}"]["{id_}"]'))
        return 'Deleted', 204
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_segments_batch_delete_validate(body, user=None, token_info=None):  # noqa: E501
    """actor_segments_batch_delete_validate

    Validation endpoint for batch segment deletion, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: ActorSegmentsBatchDeleteValidationResponse
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorSegmentsBatchDeleteBody)  # noqa: E501
        pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
            
        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                if not db_seg.exists(pattern):
                    return f'Segment collection {pattern} not found, DB is inconsistent', 404

            ret = ActorSegmentsBatchDeleteValidationResponse(id_invalid=[], value_not_found=[])
            for id_ in body.ids:
                if not db_data.exists(id_):
                    ret.id_invalid.append(id_)
                elif db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is None:
                    ret.value_not_found.append(id_)
        return ret, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_segments_batch_get(body, user=None, token_info=None):  # noqa: E501
    """actor_segments_batch_get

    Returns a batch of segment collections given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: Dict[str, List[ActorSegmentCollection]]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorSegmentsBatchGetBody)  # noqa: E501
        pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)

        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            all_segcols = db_data.json().mget(body.ids, Path('segmentCollections'))
        
        for i in range(len(all_segcols)):
            if all_segcols[i] is None:
                continue
            segcols = all_segcols[i]
            all_segcols[i] = [util.deserialize(v, ActorSegmentCollection) for v in dpath.util.values(segcols, pattern)]
        return all_segcols, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_segments_batch_post(body, user=None, token_info=None):  # noqa: E501
    """actor_segments_batch_post

    Submits a segment collection for each actor ID. # noqa: E501

    :param body: Map of IDs and segment collections
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorSegmentCollection) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            for id_, body in bodies.items():
                pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if not db_data.exists(id_):
                    return f'ID {id_} does not exist, nothing is done', 404
                if db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is not None:
                    return f'Segment collection {pattern} already exists in {id_}, nothing is done', 409
            
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                for id_, body in bodies.items():
                    pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
                    if not db_seg.exists(pattern):
                        segcol = UiucSegmentCollection(collection_name=body.collection_name, 
                                                    provider_name=body.provider_name, 
                                                    version=body.version, 
                                                    segments={k: {id_: v} for k, v in body.segments.items()})
                        db_seg.json().set(pattern, Path.rootPath(), util.serialize(segcol))
                    else:
                        segs = db_seg.json().objkeys(pattern, Path('segments'))
                        for seg in segs:
                            if db_seg.json().type(pattern, Path(f'segments["{seg}"]["{id_}"]')) is not None and seg not in body.segments:
                                db_seg.json().delete(pattern, Path(f'segments["{seg}"]["{id_}"]'))
                            elif seg in body.segments:
                                db_seg.json().set(pattern, Path(f'segments["{seg}"]["{id_}"]'), body.segments[seg])
                    db_data.json().set(id_, Path(f'segmentCollections["{pattern}"]'), util.serialize(body))
        return 'Created', 201
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_segments_batch_post_validate(body, user=None, token_info=None):  # noqa: E501
    """actor_segments_batch_post_validate

    Validation endpoint for batch segment creation, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: ActorSegmentsBatchValidationResponse
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorSegmentCollection) for k, v in connexion.request.get_json().items()}  # noqa: E501

        seen_set = set()
        ret = ActorSegmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found=None, value_existed={})
        db_data = util.get_db(db_name='actor_data')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            for id_, body in bodies.items():
                pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    ret.value_invalid[id_] = body
                elif not db_data.exists(id_):
                    ret.id_invalid[id_] = body
                elif db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is not None or (id_, pattern) in seen_set:
                    ret.value_existed[id_] = body
                else:
                    seen_set.add((id_, pattern))
        return ret, 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_segments_batch_put(body, user=None, token_info=None):  # noqa: E501
    """actor_segments_batch_put

    Updates a segment collection for each actor ID. # noqa: E501

    :param body: Map of IDs and segment collections
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorSegmentCollection) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            for id_, body in bodies.items():
                pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if not db_data.exists(id_):
                    return f'ID {id_} does not exist, nothing is done', 404
                if db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is None:
                    return f'Segment collection {pattern} not found in {id_}, nothing is done', 409
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                for id_, body in bodies.items():
                    if not db_seg.exists(pattern):
                        return f'Segment collection {pattern} does not exist', 404

                for id_, body in bodies.items():
                    pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
                    segs = db_seg.json().objkeys(pattern, Path('segments'))
                    for seg in segs:
                        if db_seg.json().type(pattern, Path(f'segments["{seg}"]["{id_}"]')) is not None and seg not in body.segments:
                            db_seg.json().delete(pattern, Path(f'segments["{seg}"]["{id_}"]'))
                        elif seg in body.segments:
                            db_seg.json().set(pattern, Path(f'segments["{seg}"]["{id_}"]'), body.segments[seg])
                    db_data.json().set(id_, Path(f'segmentCollections["{pattern}"]'), util.serialize(body))
        return 'Created', 201
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_segments_batch_put_validate(body, user=None, token_info=None):  # noqa: E501
    """actor_segments_batch_put_validate

    Validation endpoint for batch segment update, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: ActorSegmentsBatchValidationResponse
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorSegmentCollection) for k, v in connexion.request.get_json().items()}  # noqa: E501

        ret = ActorSegmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found=None, value_existed={})
        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
                for id_, body in bodies.items():
                    pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
                    if pattern.find('*') != -1:
                        ret.value_invalid[id_] = body
                    elif not db_data.exists(id_):
                        ret.id_invalid[id_] = body
                    elif db_data.json().type(id_, Path(f'segmentCollections["{pattern}"]')) is None:
                        ret.value_not_found[id_] = body
                    elif not db_seg.exists(pattern):
                        ret.value_not_found[id_] = body
        return ret, 200
    return 'Bad request', 400
