import connexion
import six
import dpath.util

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
from uiuc_incas_server.models.message_batch_get_body import MessageBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_id_response import MessageIdResponse  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server import util


@util.generic_db_lock_decor
def message_batch_get(body, user=None, token_info=None):  # noqa: E501
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
        # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        available_metas = util.get_all_keys(db_meta, pattern)

        db_data = util.get_db(db_name='message_data')
        # with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
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
def message_count_get(media_type, user=None, token_info=None):  # noqa: E501
    """message_count_get

    Return the number of message IDs available. # noqa: E501

    :param media_type: Type of entity to retrieve
    :type media_type: str

    :rtype: int
    """
    db_idx = util.get_db(db_name='index')
    # with db_idx.lock('db_index_lock', blocking_timeout=5) as lock:
    cnt = util.count_keys(db_idx, f'forward:message:{media_type.lower()}:*')
    return cnt, 200


@util.generic_db_lock_decor
def message_id_get(id_, with_enrichment=None, enrichment_name=None, provider_name=None, version=None, dev=None, user=None, token_info=None):  # noqa: E501
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
    # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
    available_metas = util.get_all_keys(db_meta, pattern)

    db_data = util.get_db(db_name='message_data')
    # with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock:
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
def message_list_get(begin, end, media_type, user=None, token_info=None):  # noqa: E501
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
    # with db_idx.lock('db_index_lock', blocking_timeout=5) as lock:
    keys = ['forward:message:{}:{}'.format(media_type.lower(), i) for i in range(begin, end)]
    records = db_idx.json().mget(keys, Path.rootPath())
    ret = [util.deserialize(x, MessageIdResponse) for x in records]
    return ret, 200
