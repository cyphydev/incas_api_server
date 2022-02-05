import connexion
import six
import dpath.util
from itertools import chain

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.enrichment import Enrichment  # noqa: E501
from uiuc_incas_server.models.enrichment_meta import EnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_delete_body import EnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_delete_validation_response import EnrichmentsBatchDeleteValidationResponse  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_get_body import EnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_validation_response import EnrichmentsBatchValidationResponse  # noqa: E501
from uiuc_incas_server import util

def generic_enrichments_batch_delete(prefix, body, return_code=204):
    pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
    if pattern.find('*') != -1:
        return 'Bad request', 400
    
    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    if db_meta.exists(pattern):
        return 'Enrichment meta must be deleted first', 400

    db_data = util.get_db(db_name=f'{prefix}_data')
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    for id_ in body.ids:
        if not db_data.exists(id_):
            return f'ID {id_} not found, nothing is done', 404
        if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
            return f'Enrichment {pattern} not found in {id_}, nothing is done', 404
    for id_ in body.ids:
        db_data.json().delete(id_, Path(f'enrichments["{pattern}"]'))
    return 'Deleted', return_code

def generic_enrichments_batch_delete_validate(prefix, body, return_code=200):
    pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
    if pattern.find('*') != -1:
        return 'Bad request', 400
    
    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    if db_meta.exists(pattern):
        return 'Enrichment meta must be deleted first', 400

    ret = EnrichmentsBatchDeleteValidationResponse(id_invalid=[], value_not_found=[])
    db_data = util.get_db(db_name=f'{prefix}_data')
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    for id_ in body.ids:
        if not db_data.exists(id_):
            ret.id_invalid.append(id_)
        if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
            ret.value_not_found.append(id_)
    return ret, 200


def generic_enrichments_batch_get(prefix, body, return_code=200):
    pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)

    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    available_metas = util.get_all_keys(db_meta, pattern)

    db_data = util.get_db(db_name=f'{prefix}_data')
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    all_enrichments = db_data.json().mget(body.ids, Path('enrichments'))

    for i in range(len(all_enrichments)):
        if all_enrichments[i] is None:
            continue
        enrichments = all_enrichments[i]
        if not body.dev:
            enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
        all_enrichments[i] = [util.deserialize(v, Enrichment) for v in dpath.util.values(enrichments, pattern)]
    return all_enrichments, return_code


def generic_enrichments_batch_post(prefix, bodies, return_code=201):
    db_data = util.get_db(db_name=f'{prefix}_data')
    db_meta = util.get_db(db_name='meta')
    
    all_patterns = set()
    exist_status = dict()
    for body in bodies.values():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        all_patterns.add(pattern)
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    for pattern in all_patterns:
        exist_status[pattern] = True if db_meta.exists(pattern) else False
            
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    for id_, body in bodies.items():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        if not db_data.exists(id_):
            return f'ID {id_} does not exist, nothing is done', 404
        if exist_status[pattern] and db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
            return f'Enrichment {pattern} already exists in {id_}, nothing is done', 409
    for id_, body in bodies.items():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
    return 'Created', return_code


def generic_enrichments_batch_post_validate(prefix, body, return_code=200):
    ret = EnrichmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found=None, value_existed={})
    db_data = util.get_db(db_name=f'{prefix}_data')
    db_meta = util.get_db(db_name='meta')
    
    all_patterns = set()
    exist_status = dict()
    for body in bodies.values():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        all_patterns.add(pattern)
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    for pattern in all_patterns:
        exist_status[pattern] = True if db_meta.exists(pattern) else False
        
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    for id_, body in bodies.items():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            ret.value_invalid[id_] = body
        if not db_data.exists(id_):
            ret.id_invalid[id_] = body
        if exist_status[pattern] and db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
            ret.value_existed[id_] = body
    return ret, return_code


def generic_enrichments_batch_put(prefix, body, return_code=200):
    db_data = util.get_db(db_name=f'{prefix}_data')
    db_meta = util.get_db(db_name='meta')
    
    all_patterns = set()
    exist_status = dict()
    for body in bodies.values():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        all_patterns.add(pattern)
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    for pattern in all_patterns:
        exist_status[pattern] = True if db_meta.exists(pattern) else False
            
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    for id_, body in bodies.items():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        if not db_data.exists(id_):
            return f'ID {id_} does not exist, nothing is done', 404
        if exist_status[pattern] and db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
            return f'Enrichment {pattern} not found in {id_}, nothing is done', 404
    for id_, body in bodies.items():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
    return 'Updated', return_code


def generic_enrichments_batch_put_validate(prefix, body, return_code=200):
    ret = EnrichmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found={}, value_existed=None)
    db_data = util.get_db(db_name=f'{prefix}_data')
    db_meta = util.get_db(db_name='meta')
    
    all_patterns = set()
    exist_status = dict()
    for body in bodies.values():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        all_patterns.add(pattern)
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    for pattern in all_patterns:
        exist_status[pattern] = True if db_meta.exists(pattern) else False
            
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    for id_, body in bodies.items():
        pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            ret.value_invalid[id_] = body
        if not db_data.exists(id_):
            ret.id_invalid[id_] = body
        if exist_status[pattern] and db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
            ret.value_not_found[id_] = body
    return ret, return_code


def generic_enrichments_meta_delete(prefix, enrichment_name, provider_name, version, return_code=204):
    pattern = util.get_enrichment_pattern(prefix, enrichment_name, provider_name, version)
    if pattern.find('*') != -1:
        return 'Bad request', 400
    
    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    if not db_meta.exists(pattern):
        return 'Key not found', 404
    db_meta.json().delete(pattern, Path.rootPath())
    return 'Deleted', return_code


def generic_enrichments_meta_get(prefix, enrichment_name=None, provider_name=None, version=None, return_code=200):
    pattern = util.get_enrichment_pattern(prefix, enrichment_name, provider_name, version)

    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    ks = util.get_all_keys(db_meta, pattern)
    if len(ks) == 0:
        return 'No keys found', 404
        
    records = db_meta.json().mget(ks, Path.rootPath())
    for i in range(len(records)):
        if records[i] is None:
            continue
        records[i] = util.deserialize(records[i], EnrichmentMeta)
    return records, return_code


def generic_enrichments_meta_post(prefix, body, return_code=201):
    pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    if db_meta.exists(pattern):
        return 'Key already exists', 409
    db_meta.json().set(pattern, Path.rootPath(), util.serialize(body))
    return "Created", return_code


def generic_enrichments_meta_put(prefix, body, return_code=200):
    pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    if not db_meta.exists(pattern):
        return 'Key not found', 404
    db_meta.json().set(pattern, Path.rootPath(), util.serialize(body))
    return "Updated", return_code


def message_id_enrichments_delete(prefix, id_, enrichment_name, provider_name, version, return_code=204):
    pattern = util.get_enrichment_pattern(prefix, enrichment_name, provider_name, version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    if db_meta.exists(pattern):
        return 'Enrichment meta must be deleted first', 400

    db_data = util.get_db(db_name=f'{prefix}_data')
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    if not db_data.exists(id_):
        return 'ID not found', 404
    if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
        return 'Enrichment not found', 404
    db_data.json().delete(id_, Path(f'enrichments["{pattern}"]'))
    return 'Deleted', return_code


def message_id_enrichments_get(prefix, id_, enrichment_name=None, provider_name=None, version=None, dev=None, return_code=200):
    pattern = util.get_enrichment_pattern(prefix, enrichment_name, provider_name, version)

    db_meta = util.get_db(db_name='meta')
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    available_metas = util.get_all_keys(db_meta, pattern)

    db_data = util.get_db(db_name=f'{prefix}_data')
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    if not db_data.exists(id_):
        return 'ID does not exist', 404
    enrichments = db_data.json().get(id_, Path('enrichments'))
    
    if not dev:
        enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
    ret = [util.deserialize(v, Enrichment) for v in dpath.util.values(enrichments, pattern)]
    return ret, return_code


def message_id_enrichments_post(prefix, body, id_, return_code=201):
    pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_data = util.get_db(db_name=f'{prefix}_data')
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    if not db_data.exists(id_):
        return 'ID does not exist', 404
    if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
        return 'Enrichment already exists', 409
    db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
    return 'Created', return_code


def message_id_enrichments_put(prefix, body, id_, return_code=200):
    pattern = util.get_enrichment_pattern(prefix, body.enrichment_name, body.provider_name, body.version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_data = util.get_db(db_name=f'{prefix}_data')
    # with db_data.lock(f'db_{prefix}_data_lock', blocking_timeout=5) as lock:
    if not db_data.exists(id_):
        return 'ID does not exist', 404
    if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
        return 'Enrichment not found', 404
    db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
    return 'Updated', return_code
