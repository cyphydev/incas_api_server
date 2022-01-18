import connexion
import six
import dpath.util

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.actor_batch_get_body import ActorBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichment import ActorEnrichment  # noqa: E501
from uiuc_incas_server.models.actor_enrichment_meta import ActorEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_delete_body import ActorEnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_get_body import ActorEnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.uiuc_actor import UiucActor  # noqa: E501
from uiuc_incas_server import util

get_db = connexion.utils.get_function_from_name('uiuc_incas_server.util.get_db')

def get_all_keys(db, pattern):
    cur, kks = 0, []
    cur, ks = db.execute_command(f'SCAN {cur} MATCH {pattern} COUNT 10000')
    cur = int(cur)
    kks.extend(map(lambda x: x.decode('utf-8'), ks))
    while cur != 0:
        cur, ks = db.execute_command(f'SCAN {cur} MATCH {pattern} COUNT 10000')
        cur = int(cur)
        kks.extend(map(lambda x: x.decode('utf-8'), ks))
    return kks

def actor_batch_get(body):  # noqa: E501
    """actor_batch_get

    Returns a batch of actors given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: List[UiucActor]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorBatchGetBody)  # noqa: E501
        if body.enrichment_name is None:
            body.enrichment_name = '*'
        if body.provider_name is None:
            body.provider_name = '*'
        if body.version is None:
            body.version = '*'

        pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
        db_meta = get_db(db_name='meta')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
                available_metas = get_all_keys(db_meta, pattern)
        except LockError:
            return 'Lock not acquired', 500

        db_data = get_db(db_name='actor_data')
        try:
            with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
                records = db_data.json().mget(body.ids, Path.rootPath())
            for i in range(len(records)):
                if records[i] is None:
                    continue
                if body.with_enrichment:
                    if body.dev:
                        enrichments = records[i]['enrichments']
                    else:
                        enrichments = {k: v for k, v in records[i]['enrichments'].items() if k in available_metas}
                    records[i]['enrichments'] = dpath.util.values(enrichments, pattern)
                else:
                    records[i]['enrichments'] = []
                records[i] = util.deserialize(records[i], UiucActor)

            return records, 200
        except LockError:
            return 'Lock not acquired', 500
            
    return 'Bad request', 400


def actor_count_get(entity_type):  # noqa: E501
    """actor_count_get

    Return the number of actor IDs available. # noqa: E501


    :rtype: int
    """
    db_idx = get_db(db_name='index')
    try:
        with db_idx.lock('db_index_lock', blocking_timeout=5) as lock:
            cnt, cur = 0, 0
            cur, ks = db_idx.execute_command(f'SCAN {cur} MATCH actor:{entity_type.lower()}:* COUNT 10000')
            cur = int(cur)
            cnt += len(ks)
            while cur != 0:
                cur, ks = db_idx.execute_command(f'SCAN {cur} MATCH actor:{entity_type.lower()}:* COUNT 10000')
                cur = int(cur)
                cnt += len(ks)
    except LockError:
        return 'Lock not acquired', 500
    return cnt, 200


def actor_enrichments_batch_delete(body):  # noqa: E501
    """actor_enrichments_batch_delete

    Deletes a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentsBatchDeleteBody)  # noqa: E501
        
        pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
        if pattern.find('*') != -1:
            return 'Bad request', 400
        db_meta = get_db(db_name='meta')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
                if db_meta.exists(pattern):
                    return 'Enrichment meta must be deleted first', 400
        except LockError:
            return 'Lock not acquired', 500

        db_data = get_db(db_name='actor_data')
        try:
            with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
                for id_ in body.ids:
                    if not db_data.exists(id_):
                        return f'ID {id_} not found, nothing is done', 404
                    if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                        return f'Enrichment {pattern} not found in {id_}, nothing is done', 404
                for id_ in body.ids:
                    db_data.json().delete(id_, Path(f'enrichments["{pattern}"]'))
                return 'Deleted', 204
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_enrichments_batch_get(body):  # noqa: E501
    """actor_enrichments_batch_get

    Returns a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: Dict[str, List[ActorEnrichment]]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentsBatchGetBody)  # noqa: E501
        if body.enrichment_name is None:
            body.enrichment_name = '*'
        if body.provider_name is None:
            body.provider_name = '*'
        if body.version is None:
            body.version = '*'
        pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_meta = get_db(db_name='meta')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
                available_metas = get_all_keys(db_meta, pattern)
        except LockError:
            return 'Lock not acquired', 500

        db_data = get_db(db_name='actor_data')
        try:
            with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
                all_enrichments = db_data.json().mget(body.ids, Path('enrichments'))

            for i in range(len(all_enrichments)):
                if all_enrichments[i] is None:
                    continue
                enrichments = all_enrichments[i]
                if not body.dev:
                    enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
                all_enrichments[i] = [util.deserialize(v, ActorEnrichment) 
                    for v in dpath.util.values(
                        enrichments, 
                        pattern
                    )]

            return all_enrichments, 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400

def actor_enrichments_batch_post(body):  # noqa: E501
    """actor_enrichments_batch_post

    Submits a enrichment for each actor ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = get_db(db_name='actor_data')
        try:
            with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
                for id_, body in bodies.items():
                    pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
                    if pattern.find('*') != -1:
                        return 'Bad request', 400
                    if not db_data.exists(id_):
                        return f'ID {id_} does not exist, nothing is done', 404
                    if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
                        return f'Enrichment {pattern} already exists in {id_}, nothing is done', 409
                for id_, body in bodies.items():
                    pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
                    db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
                return 'Created', 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_enrichments_batch_put(body):  # noqa: E501
    """actor_enrichments_batch_put

    Updates a enrichment for each actor ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, ActorEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = get_db(db_name='actor_data')
        try:
            with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
                for id_, body in bodies.items():
                    pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
                    if pattern.find('*') != -1:
                        return 'Bad request', 400
                    if not db_data.exists(id_):
                        return f'ID {id_} does not exist, nothing is done', 404
                    if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                        return f'Enrichment {pattern} not found in {id_}, nothing is done', 404
                for id_, body in bodies.items():
                    pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
                    db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
                return 'Updated', 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_enrichments_meta_delete(enrichment_name, provider_name, version):  # noqa: E501
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
    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            pattern = f'actor:{enrichment_name}:{provider_name}:{version}'
            if pattern.find('*') != -1:
                return 'Bad request', 400
            if not db_meta.exists(pattern):
                return 'Key not found', 404
            db_meta.json().delete(pattern, Path.rootPath())
        return 'Deleted', 204
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


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
    if enrichment_name is None:
        enrichment_name = '*'
    if provider_name is None:
        provider_name = '*'
    if version is None:
        version = '*'
    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            ks = get_all_keys(db_meta, f'actor:{enrichment_name}:{provider_name}:{version}')
            if len(ks) == 0:
                return 'No keys found', 404
            records = db_meta.json().mget(ks, Path.rootPath())
            for i in range(len(records)):
                records[i] = util.deserialize(records[i], ActorEnrichmentMeta)
            return records, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_enrichments_meta_post(body):  # noqa: E501
    """actor_enrichments_meta_post

    Submits an actor enrichment meta (post after all actors have been added). # noqa: E501

    :param body: The new enrichment meta to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentMeta)  # noqa: E501
        db_meta = get_db(db_name='meta')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
                pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if db_meta.exists(pattern):
                    return 'Key already exists', 409
                db_meta.json().set(pattern, Path.rootPath(), util.serialize(body))
                return "Created", 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_enrichments_meta_put(body):  # noqa: E501
    """actor_enrichments_meta_put

    Updates an actor enrichment meta (after all actors have been added) by providerName, enrichmentName and version. # noqa: E501

    :param body: The new enrichment meta to update
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichmentMeta)  # noqa: E501
        db_meta = get_db(db_name='meta')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
                pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if not db_meta.exists(pattern):
                    return 'Key not found', 404
                db_meta.json().set(pattern, Path.rootPath(), util.serialize(body))
                return "Updated", 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


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
    pattern = f'actor:{enrichment_name}:{provider_name}:{version}'
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if db_meta.exists(pattern):
                return 'Enrichment meta must be deleted first', 400
    except LockError:
        return 'Lock not acquired', 500
    db_data = get_db(db_name='actor_data')
    try:
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID not found', 404
            if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                return 'Enrichment not found', 404
            db_data.json().delete(id_, Path(f'enrichments["{pattern}"]'))
            return 'Deleted', 204
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


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
    if enrichment_name is None:
        enrichment_name = '*'
    if provider_name is None:
        provider_name = '*'
    if version is None:
        version = '*'
    pattern = f'actor:{enrichment_name}:{provider_name}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_metas = get_all_keys(db_meta, pattern)
    except LockError:
        return 'Lock not acquired', 500
    db_data = get_db(db_name='actor_data')
    try:
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            enrichments = db_data.json().get(id_, Path('enrichments'))
        if not dev:
            enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
        ret = [util.deserialize(v, ActorEnrichment) for v in dpath.util.values(enrichments, pattern)]
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_id_enrichments_post(body, id_):  # noqa: E501
    """actor_id_enrichments_post

    Submits a new enrichment for specific actor. # noqa: E501

    :param body: The new enrichment to add
    :type body: dict | bytes
    :param id: Actor ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorEnrichment)  # noqa: E501
        pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
        if pattern.find('*') != -1:
            return 'Bad request', 400
        db_data = get_db(db_name='actor_data')
        try:
            with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
                if not db_data.exists(id_):
                    return 'ID does not exist', 404
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
                    return 'Enrichment already exists', 409

                db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
                return 'Created', 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


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
        body = util.deserialize(connexion.request.get_json(), ActorEnrichment)  # noqa: E501
        pattern = f'actor:{body.enrichment_name}:{body.provider_name}:{body.version}'
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_data = get_db(db_name='actor_data')
        try:
            with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
                if not db_data.exists(id_):
                    return 'ID does not exist', 404
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    return 'Enrichment not found', 404
                    
                db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
                return 'Updated', 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


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
    if enrichment_name is None:
        enrichment_name = '*'
    if provider_name is None:
        provider_name = '*'
    if version is None:
        version = '*'
    pattern = f'actor:{enrichment_name}:{provider_name}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_metas = get_all_keys(db_meta, pattern)
    except LockError:
        return 'Lock not acquired', 500
    db_data = get_db(db_name='actor_data')
    try:
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'Key does not exist', 404
            record = db_data.json().get(id_, Path.rootPath())
        if with_enrichment:
            if dev:
                enrichments = record['enrichments']
            else:
                enrichments = {k: v for k, v in record['enrichments'].items() if k in available_metas}
            record['enrichments'] = dpath.util.values(enrichments, pattern)
        else:
            record['enrichments'] = []
        ret = util.deserialize(record, UiucActor)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_list_get(begin, end, entity_type):  # noqa: E501
    """actor_list_get

    Return list of actor IDs available in [begin, end). # noqa: E501

    :param begin: Begin
    :type begin: int
    :param end: End
    :type end: int
    :param entity_type: Entity_type
    :type entity_type: str

    :rtype: List[str]
    """
    db_idx = get_db(db_name='index')
    try:
        with db_idx.lock('db_index_lock', blocking_timeout=5) as lock:
            keys = ['actor:{}:{}'.format(entity_type.lower(), i) for i in range(begin, end)]
            ret = db_idx.json().mget(keys, Path.rootPath())
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400
