import connexion
import six
import dpath.util

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.uiuc_segment_collection import UiucSegmentCollection  # noqa: E501
from uiuc_incas_server.models.uiuc_segment_collection_meta import UiucSegmentCollectionMeta  # noqa: E501
from uiuc_incas_server import util


@util.generic_db_lock_decor
def segment_collection_id_delete(id_, user=None, token_info=None):  # noqa: E501
    """segment_collection_id_delete

    Deletes the segment collection by id. # noqa: E501

    :param id: Segment collection ID
    :type id: str

    :rtype: None
    """
    db_data = util.get_db(db_name='actor_data')
    db_seg = util.get_db(db_name='segment')
    with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock1:
        if not db_seg.exists(id_):
            return 'Key does not exist', 404
        record = db_seg.json().get(id_, Path.rootPath())
        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock2:
            for actors in record.segments.values():
                for actor in actors.keys():
                    if db_data.json().type(actor, Path(f'segment_collections["{id_}"]')) is not None:
                        db_data.json().delete(actor, Path(f'segment_collections["{id_}"]'))
            db_seg.delete(id_, Path.rootPath())
    return 'Deleted', 204


@util.generic_db_lock_decor
def segment_collection_id_get(id_, user=None, token_info=None):  # noqa: E501
    """segment_collection_id_get

    Gets a segment collection by id. # noqa: E501

    :param id: Segment collection ID
    :type id: str

    :rtype: UiucSegmentCollection
    """
    db_seg = util.get_db(db_name='segment')
    with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
        if not db_seg.exists(id_):
            return 'Key does not exist', 404
        record = db_seg.json().get(id_, Path.rootPath())
    ret = util.deserialize(record, UiucSegmentCollection)
    return ret, 200


@util.generic_db_lock_decor
def segment_collection_id_put(body, id_, user=None, token_info=None):  # noqa: E501
    """segment_collection_id_put

    Update basic segment collection information by id. # noqa: E501

    :param body: The segment collection meta
    :type body: dict | bytes
    :param id: Segment collection ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), UiucSegmentCollectionMeta)  # noqa: E501
        pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
        if pattern != id_:
            return 'Key does not meta', 400

        db_seg = util.get_db(db_name='segment')
        with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
            if not db_seg.exists(id_):
                return 'Key does not exist', 404
            db_seg.json().set(id_, Path('description'), body.description)
            db_seg.json().set(id_, Path('segment_descriptions'), body.segment_descriptions)
        return 'Updated', 200
    return 'Bad request', 400


@util.generic_db_lock_decor
def segment_collection_list_get(collection_name=None, provider_name=None, version=None, user=None, token_info=None):  # noqa: E501
    """segment_collection_list_get

    Return list of available segment collection keys by collectionName, providerName, and version. # noqa: E501

    :param collection_name: 
    :type collection_name: str
    :param provider_name: 
    :type provider_name: str
    :param version: 
    :type version: str

    :rtype: List[str]
    """
    pattern = util.get_collection_pattern('actor', collection_name, provider_name, version)
    db_seg = util.get_db(db_name='segment')
    with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
        seg_ids = util.get_all_keys(db_seg, pattern)
    return seg_ids, 200


@util.generic_db_lock_decor
def segment_collection_post(body, user=None, token_info=None):  # noqa: E501
    """segment_collection_post

    Add a new segment collection. # noqa: E501

    :param body: The new segment collection to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), UiucSegmentCollectionMeta)  # noqa: E501
        pattern = util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400

        db_seg = util.get_db(db_name='segment')
        with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
            if db_seg.exists(pattern):
                return 'Segment collection already exists', 409
            segcol = UiucSegmentCollection(
                description=body.description,
                collection_name=body.collection_name,
                provider_name=body.provider_name,
                version=body.version,
                segment_descriptions=body.segment_descriptions,
                segments={})
            db_seg.json().set(pattern, Path.rootPath(), util.serialize(segcol))
        return 'Created', 201
    return 'Bad request', 400
