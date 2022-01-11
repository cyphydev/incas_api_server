import connexion
import six
import dpath.util

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.enrichments_batch_delete_body import EnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.enrichments_batch_get_body import EnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_batch_get_body import MessageBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_enrichment import MessageEnrichment  # noqa: E501
from uiuc_incas_server.models.message_enrichment_meta import MessageEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server.models.uiuc_message_db import UiucMessageDB  # noqa: E501
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

def message_batch_get(body):  # noqa: E501
    """message_batch_get

    Returns a batch of messages given a list of IDs and specifications. # noqa: E501

    :param body: List of IDs and specifications
    :type body: dict | bytes

    :rtype: List[UiucMessage]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageBatchGetBody)  # noqa: E501
        pattern = f'message:{body.enrichment_name}:{body.provider_name}:{body.version}'
        db_data = get_db(db_name='message_data')
        try:
            with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
                records = db_data.json().mget(body.ids, Path.rootPath())
                for i in range(len(records)):
                    records[i]['enrichments'] = dpath.util.values(records[i]['enrichments'], pattern)
                    records[i] = util.deserialize(records[i], UiucMessage)
                return records, 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def message_count_get(media_type):  # noqa: E501
    """message_count_get

    Return the number of message IDs available. # noqa: E501

    :param media_type: Type of entity to retrieve
    :type media_type: str

    :rtype: int
    """
    db_idx = get_db(db_name='index')
    try:
        with db_data.lock('db_index_lock', blocking_timeout=5) as lock:
            cnt, cur = 0, 0
            cur, ks = db_idx.execute_command(f'SCAN {cur} MATCH message:{media_type.lower()}:* COUNT 10000')
            cur = int(cur)
            cnt += len(ks)
            while cur != 0:
                cur, ks = db_idx.execute_command(f'SCAN {cur} MATCH message:{media_type.lower()}:* COUNT 10000')
                cur = int(cur)
                cnt += len(ks)
    except LockError:
        return 'Lock not acquired', 500
    return cnt, 200


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
    db_meta = get_db(db_name='meta')
    try:
        with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
            k = f'message:{enrichment_name}:{provider_name}:{version}'
            if not db_meta.exists(k):
                return 'Key not found', 404
            db_meta.json().delete(k, Path.rootPath())
        return 'Deleted', 204
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


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
    if enrichment_name is None:
        enrichment_name = '*'
    if provider_name is None:
        provider_name = '*'
    if version is None:
        version = '*'
    db_meta = get_db(db_name='meta')
    try:
        with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
            ks = get_all_keys(db_meta, f'message:{enrichment_name}:{provider_name}:{version}')
            print(ks)
            if len(ks) == 0:
                return 'No keys found', 404
            records = db_meta.json().mget(ks, Path.rootPath())
            for i in range(len(records)):
                records[i] = util.deserialize(records[i], MessageEnrichmentMeta)
            return records, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def message_enrichments_meta_post(body):  # noqa: E501
    """message_enrichments_meta_post

    Submits a message enrichment meta (post after all messages have been added). # noqa: E501

    :param body: The new enrichment meta to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichmentMeta)  # noqa: E501
        db_meta = get_db(db_name='meta')
        try:
            with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
                k = f'message:{body.enrichment_name}:{body.provider_name}:{body.version}'
                if db_meta.exists(k):
                    return 'Key already exists', 409
                db_meta.json().set(k, Path.rootPath(), util.serialize(body))
                return "Created", 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def message_enrichments_meta_put(body):  # noqa: E501
    """message_enrichments_meta_put

    Updates message enrichment meta (after all messages have been added) by providerName, enrichmentName and version. # noqa: E501

    :param body: The new enrichment meta to update
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichmentMeta)  # noqa: E501
        db_meta = get_db(db_name='meta')
        try:
            with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
                k = f'message:{body.enrichment_name}:{body.provider_name}:{body.version}'
                if not db_meta.exists(k):
                    return 'Key not found', 404
                db_meta.json().set(k, Path.rootPath(), util.serialize(body))
                return "Updated", 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def message_id_enrichments_delete(id_, enrichment_name, provider_name, version):  # noqa: E501
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
    pattern = f'message:{enrichment_name}:{provider_name}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
            if db_meta.exists(pattern):
                return 'Enrichment meta must be deleted first', 400
    except LockError:
        return 'Lock not acquired', 500
    db_data = get_db(db_name='message')
    try:
        with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID not found', 404
            record = db_data.json().get(id_, Path.rootPath())
            if not pattern in record['enrichments']:
                return 'Enrichment not found', 404
            del(record['enrichments'][pattern])
            db_data.json().set(id_, Path.rootPath(), record)
            return 'Deleted', 204
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


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
    if enrichment_name is None:
        enrichment_name = '*'
    if provider_name is None:
        provider_name = '*'
    if version is None:
        version = '*'
    pattern = f'message:{enrichment_name}:{provider_name}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_metas = get_all_keys(db_meta, pattern)
    except LockError:
        return 'Lock not acquired', 500
    db_data = get_db(db_name='message_data')
    try:
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'ID does not exist', 404
            record = db_data.json().get(id_, Path.rootPath())
        if dev:
            enrichments = record['enrichments']
        else:
            enrichments = {k: v for k, v in record['enrichments'].items() if k in available_metas}
        ret = [util.deserialize(v, MessageEnrichment) 
            for v in dpath.util.values(
                enrichments, 
                pattern
            )]
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def message_id_enrichments_post(body, id_):  # noqa: E501
    """message_id_enrichments_post

    Submits a new enrichment for specific message. # noqa: E501

    :param body: The new enrichment to add
    :type body: dict | bytes
    :param id: Message ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichment)  # noqa: E501
        pattern = f'message:{body.enrichment_name}:{body.provider_name}:{body.version}'
        db_data = get_db(db_name='message_data')
        try:
            with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
                if not db_data.exists(id_):
                    return 'ID does not exist', 404
                record = db_data.json().get(id_, Path.rootPath())
            if pattern in record['enrichments']:
                return 'Enrichment already exists', 409
            record['enrichments'][pattern] = util.serialize(body)
            db_data.json().set(id_, Path.rootPath(), record)
            return 'Created', 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def message_id_enrichments_put(body, id_):  # noqa: E501
    """message_id_enrichments_put

    Update a enrichment for specific message by type, providerName and version. # noqa: E501

    :param body: The new enrichments to update
    :type body: dict | bytes
    :param id: Message ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageEnrichment)  # noqa: E501
        pattern = f'message:{body.enrichment_name}:{body.provider_name}:{body.version}'
        db_data = get_db(db_name='message_data')
        try:
            with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
                if not db_data.exists(id_):
                    return 'ID does not exist', 404
                record = db_data.json().get(id_, Path.rootPath())
            if pattern not in record['enrichments']:
                return 'Enrichment does not exist', 404
            record['enrichments'][pattern] = util.serialize(body)
            db_data.json().set(id_, Path.rootPath(), record)
            return 'Updated', 200
        except LockError:
            return 'Lock not acquired', 500
    return 'do some magic!'


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
    if enrichment_name is None:
        enrichment_name = '*'
    if provider_name is None:
        provider_name = '*'
    if version is None:
        version = '*'
    pattern = f'message:{enrichment_name}:{provider_name}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_data.lock('db_meta_lock', blocking_timeout=5) as lock:
            available_metas = get_all_keys(db_meta, pattern)
    except LockError:
        return 'Lock not acquired', 500
    db_data = get_db(db_name='message_data')
    try:
        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
            if not db_data.exists(id_):
                return 'Key does not exist', 404
            record = db_data.json().get(id_, Path.rootPath())
        if dev:
            enrichments = record['enrichments']
        else:
            enrichments = {k: v for k, v in record['enrichments'].items() if k in available_metas}
        record['enrichments'] = dpath.util.values(enrichments, pattern)
        ret = util.deserialize(record, UiucMessage)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def message_list_get(begin, end, media_type):  # noqa: E501
    """message_list_get

    Return list of message IDs available in [begin, end). # noqa: E501

    :param begin: Begin
    :type begin: int
    :param end: End
    :type end: int
    :param media_type: Type of entity to retrieve
    :type media_type: str

    :rtype: List[str]
    """
    db_idx = get_db(db_name='index')
    try:
        with db_data.lock('db_index_lock', blocking_timeout=5) as lock:
            keys = ['message:{}:{}'.format(media_type.lower(), i) for i in range(begin, end)]
            ret = db_idx.json().mget(keys, Path.rootPath())
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400
