import connexion
import six
import dpath.util

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.message_batch_get_body import MessageBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_enrichment import MessageEnrichment  # noqa: E501
from uiuc_incas_server.models.message_enrichment_meta import MessageEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_delete_validation_response import MessageEnrichmentsBatchDeleteValidationResponse  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_delete_body import MessageEnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_get_body import MessageEnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_validation_response import MessageEnrichmentsBatchValidationResponse  # noqa: E501
from uiuc_incas_server.models.message_id_response import MessageIdResponse  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server import util


@util.generic_db_lock_decor
def message_batch_get(body):  # noqa: E501
    """message_batch_get

    Returns a batch of messages given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: List[UiucMessage]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageBatchGetBody)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)

        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_metas = util.get_all_keys(db_meta, pattern)

        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
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
            records[i] = util.deserialize(records[i], UiucMessage)

        return records, 200
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_count_get(media_type):  # noqa: E501
    """message_count_get

    Return the number of message IDs available. # noqa: E501

    :param media_type: Type of entity to retrieve
    :type media_type: str

    :rtype: int
    """
    db_idx = util.get_db(db_name='index')
    with db_idx.lock('db_index_lock', blocking_timeout=5) as lock:
        cnt = util.count_keys(db_idx, f'forward:message:{media_type.lower()}:*')
    return cnt, 200

@util.generic_db_lock_decor
def message_enrichments_batch_delete(body):  # noqa: E501
    """message_enrichments_batch_delete

    Deletes a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichmentsBatchDeleteBody)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if db_meta.exists(pattern):
                return 'Enrichment meta must be deleted first', 400

        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
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
def message_enrichments_batch_delete_validate(body):  # noqa: E501
    """message_enrichments_batch_delete_validate

    Validation endpoint for batch enrichment deletion, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: MessageEnrichmentsBatchDeleteValidationResponse
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichmentsBatchDeleteBody)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if db_meta.exists(pattern):
                return 'Enrichment meta must be deleted first', 400

        ret = MessageEnrichmentsBatchDeleteValidationResponse(id_invalid=[], value_not_found=[])
        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            for id_ in body.ids:
                if not db_data.exists(id_):
                    ret.id_invalid.append(id_)
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    ret.value_not_found.append(id_)
        return ret, 200
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_enrichments_batch_get(body):  # noqa: E501
    """message_enrichments_batch_get

    Returns a batch of enrichments given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: Dict[str, List[MessageEnrichment]]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichmentsBatchGetBody)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_meta = util.get_db(db_name='meta')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_metas = util.get_all_keys(db_meta, pattern)

        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            all_enrichments = db_data.json().mget(body.ids, Path('enrichments'))

        for i in range(len(all_enrichments)):
            if all_enrichments[i] is None:
                continue
            enrichments = all_enrichments[i]
            if not body.dev:
                enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
            all_enrichments[i] = [util.deserialize(v, MessageEnrichment) for v in dpath.util.values(enrichments, pattern)]
        return all_enrichments, 200
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_enrichments_batch_post(body):  # noqa: E501
    """message_enrichments_batch_post

    Submits a enrichment for each message ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, MessageEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if not db_data.exists(id_):
                    return f'ID {id_} does not exist, nothing is done', 404
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
                    return f'Enrichment {pattern} already exists in {id_}, nothing is done', 409
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
                db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Created', 201
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_enrichments_batch_post_validate(body):  # noqa: E501
    """message_enrichments_batch_post_validate

    Validation endpoint for batch enrichment creation, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: MessageEnrichmentsBatchValidationResponse
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, MessageEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501
        
        ret = MessageEnrichmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found=None, value_existed={})
        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    ret.value_invalid[id_] = body
                if not db_data.exists(id_):
                    ret.id_invalid[id_] = body
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
                    ret.value_existed[id_] = body
        return ret, 200
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_enrichments_batch_put(body):  # noqa: E501
    """message_enrichments_batch_put

    Updates a enrichment for each message ID. # noqa: E501

    :param body: Map of IDs and enrichments
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, MessageEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    return 'Bad request', 400
                if not db_data.exists(id_):
                    return f'ID {id_} does not exist, nothing is done', 404
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    return f'Enrichment {pattern} not found in {id_}, nothing is done', 404
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
                db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Updated', 200
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_enrichments_batch_put_validate(body):  # noqa: E501
    """message_enrichments_batch_put_validate

    Validation endpoint for batch enrichment update, successful attempt will return a token. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: MessageEnrichmentsBatchValidationResponse
    """
    if connexion.request.is_json:
        bodies = {k: util.deserialize(v, MessageEnrichment) for k, v in connexion.request.get_json().items()}  # noqa: E501

        ret = MessageEnrichmentsBatchValidationResponse(id_invalid={}, value_invalid={}, value_not_found={}, value_existed=None)
        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            for id_, body in bodies.items():
                pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
                if pattern.find('*') != -1:
                    ret.value_invalid[id_] = body
                if not db_data.exists(id_):
                    ret.id_invalid[id_] = body
                if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                    ret.value_not_found[id_] = body
        return ret, 200
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_enrichments_meta_delete(enrichment_name, provider_name, version):  # noqa: E501
    """message_enrichments_meta_delete

    Delete specific message enrichment meta by providerName, enrichmentName and version. # noqa: E501

    :param enrichment_name: 
    :type enrichment_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: str
    """
    pattern = util.get_enrichment_pattern('message', enrichment_name, provider_name, version)
    if pattern.find('*') != -1:
        return 'Bad request', 400
    
    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        if not db_meta.exists(pattern):
            return 'Key not found', 404
        db_meta.json().delete(pattern, Path.rootPath())
    return 'Deleted', 204

@util.generic_db_lock_decor
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
    pattern = util.get_enrichment_pattern('message', enrichment_name, provider_name, version)

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        ks = util.get_all_keys(db_meta, pattern)
        if len(ks) == 0:
            return 'No keys found', 404
        
        records = db_meta.json().mget(ks, Path.rootPath())
        for i in range(len(records)):
            if records[i] is None:
                continue
            records[i] = util.deserialize(records[i], MessageEnrichmentMeta)
    return records, 200

@util.generic_db_lock_decor
def message_enrichments_meta_post(body):  # noqa: E501
    """message_enrichments_meta_post

    Submits a message enrichment meta (post after all messages have been added). # noqa: E501

    :param body: The new enrichment meta to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichmentMeta)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
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
def message_enrichments_meta_put(body):  # noqa: E501
    """message_enrichments_meta_put

    Updates message enrichment meta (after all messages have been added) by providerName, enrichmentName and version. # noqa: E501

    :param body: The new enrichment meta to update
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichmentMeta)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
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
def message_id_enrichments_delete(id_,enrichment_name, provider_name, version):  # noqa: E501
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

    :rtype: str
    """
    pattern = util.get_enrichment_pattern('message', enrichment_name, provider_name, version)
    if pattern.find('*') != -1:
        return 'Bad request', 400

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        if db_meta.exists(pattern):
            return 'Enrichment meta must be deleted first', 400

    db_data = util.get_db(db_name='message_data')
    with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
        if not db_data.exists(id_):
            return 'ID not found', 404
        if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
            return 'Enrichment not found', 404
        db_data.json().delete(id_, Path(f'enrichments["{pattern}"]'))
    return 'Deleted', 204

@util.generic_db_lock_decor
def message_id_enrichments_get(id_, enrichment_name=None, provider_name=None, version=None, dev=None):  # noqa: E501
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
    pattern = util.get_enrichment_pattern('message', enrichment_name, provider_name, version)

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        available_metas = util.get_all_keys(db_meta, pattern)

    db_data = util.get_db(db_name='message_data')
    with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
        if not db_data.exists(id_):
            return 'ID does not exist', 404
        enrichments = db_data.json().get(id_, Path('enrichments'))
    
    if not dev:
        enrichments = {k: v for k, v in enrichments.items() if k in available_metas}
    ret = [util.deserialize(v, MessageEnrichment) for v in dpath.util.values(enrichments, pattern)]
    return ret, 200

@util.generic_db_lock_decor
def message_id_enrichments_post(body, id_):  # noqa: E501
    """message_id_enrichments_post

    Submits a new enrichment for specific message. # noqa: E501

    :param body: The new enrichment to add
    :type body: dict | bytes
    :param id: Message ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichment)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is not None:
                return 'Enrichment already exists', 409
            db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Created', 201
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_id_enrichments_put(body, id_):  # noqa: E501
    """message_id_enrichments_put

    Update a enrichment for specific message by type, providerName and version. # noqa: E501

    :param body: The new enrichments to update
    :type body: dict | bytes
    :param id: Message ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichment)  # noqa: E501
        pattern = util.get_enrichment_pattern('message', body.enrichment_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_data = util.get_db(db_name='message_data')
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            if db_data.json().type(id_, Path(f'enrichments["{pattern}"]')) is None:
                return 'Enrichment not found', 404
            db_data.json().set(id_, Path(f'enrichments["{pattern}"]'), util.serialize(body))
        return 'Updated', 200
    return 'Bad request', 400

@util.generic_db_lock_decor
def message_id_get(id_, with_enrichment=None, enrichment_name=None, provider_name=None, version=None, dev=None):  # noqa: E501
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
    pattern = util.get_enrichment_pattern('message', enrichment_name, provider_name, version)

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        available_metas = util.get_all_keys(db_meta, pattern)

    db_data = util.get_db(db_name='message_data')
    with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
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
    
    ret = util.deserialize(record, UiucMessage)
    return ret, 200

@util.generic_db_lock_decor
def message_list_get(begin, end, media_type):  # noqa: E501
    """message_list_get

    Return list of message IDs available in [begin, end). # noqa: E501

    :param begin: Begin
    :type begin: int
    :param end: End
    :type end: int
    :param media_type: Type of entity to retrieve
    :type media_type: str

    :rtype: List[MessageIdResponse]
    """
    db_idx = util.get_db(db_name='index')
    with db_data.lock('db_index_lock', blocking_timeout=5) as lock:
        keys = ['forward:message:{}:{}'.format(media_type.lower(), i) for i in range(begin, end)]
        records = db_idx.json().mget(keys, Path.rootPath())
    ret = [deserialize(x, MessageIdResponse) for x in records]
    return ret, 200
