import connexion
import six
import dpath.util

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.uiuc_segment_collection import UiucSegmentCollection  # noqa: E501
from uiuc_incas_server.models.actor_segment_collection import ActorSegmentCollection
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
    # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock1:
    if not db_seg.exists(id_):
        return 'Key does not exist', 404
    record = db_seg.json().get(id_, Path.rootPath())
    # with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock2:
    for actors in record['segments'].values():
        for actor in actors.keys():
            if db_data.json().type(actor, Path(f'segmentCollections["{id_}"]')) is not None:
                db_data.json().delete(actor, Path(
                    f'segmentCollections["{id_}"]'))
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
    # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
    if not db_seg.exists(id_):
        return 'Key does not exist', 404
    record = db_seg.json().get(id_, Path.rootPath())
    ret = util.deserialize(record, UiucSegmentCollection)
    return ret, 200


@util.generic_db_lock_decor
def segment_collection_id_partial_put(body, id_, user=None, token_info=None):  # noqa: E501
    """segment_collection_id_partial_put

    Update segment collection by id_, only update values that are modified in the request body. # noqa: E501

    :param body: The segment collection meta
    :type body: dict | bytes
    :param id: Segment collection ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = UiucSegmentCollection.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


@util.generic_db_lock_decor
def segment_collection_id_put(body, id_, user=None, token_info=None):  # noqa: E501
    """segment_collection_id_put

    Update segment collection by id. # noqa: E501

    :param body: The segment collection meta
    :type body: dict | bytes
    :param id: Segment collection ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), UiucSegmentCollection)  # noqa: E501
        if util.get_collection_pattern('actor', body.collection_name, body.provider_name, body.version) != id_:
            return 'Key fields cannot be modified', 400

        db_seg = util.get_db(db_name='segment')
        db_data = util.get_db(db_name='actor_data')
        
        # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
        if not db_seg.exists(id_):
            return 'Segment does not exist', 404

        all_new_actors = set()
        for seg in body.segments.values():
            for actor_id in seg.keys():
                all_new_actors.add(actor_id)

        # with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock:
        for actor_id in all_new_actors:
            if not db_data.exists(actor_id):
                return f'Actor {actor_id} does not exist', 404
                        
        all_old_actors = set()
        # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
        record = db_seg.json().get(id_, Path.rootPath())
        for actors in record['segments'].values():
            for actor in actors:
                all_old_actors.add(actor)
                    
        # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock1:
            # with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock2:
        for actor in all_old_actors:
            if db_data.json().type(actor, Path(f'segmentCollections["{id_}"]')) is not None:
                db_data.json().delete(actor, Path(f'segmentCollections["{id_}"]'))
                
        db_seg.json().set(id_, Path.rootPath(), util.serialize(body))
        actors_segs = {}
        for seg_name, actors in body.segments.items():
            for actor_id, membership in actors.items():
                if actor_id not in actors_segs:
                    actors_segs[actor_id] = {}
                actors_segs[actor_id][seg_name] = membership
        for actor_id, segs in actors_segs.items():
            actor_seg_body = ActorSegmentCollection(
                provider_name=body.provider_name,
                collection_name=body.collection_name,
                version=body.version,
                segments=segs
            )
            db_data.json().set(actor_id, Path(
                f'segmentCollections["{id_}"]'), util.serialize(actor_seg_body))
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
    pattern = util.get_collection_pattern(
        'actor', collection_name, provider_name, version)
    db_seg = util.get_db(db_name='segment')
    # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock:
    seg_ids = util.get_all_keys(db_seg, pattern)
    return list(seg_ids), 200


@util.generic_db_lock_decor
def segment_collection_post(body, user=None, token_info=None):  # noqa: E501
    """segment_collection_post

    Add a new segment collection. # noqa: E501

    :param body: The new segment collection to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), UiucSegmentCollection)  # noqa: E501
        pattern = util.get_collection_pattern(
            'actor', body.collection_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')

        # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock1:
        if db_seg.exists(pattern):
            return 'Segment collection already exists', 409
        
        all_new_actors = set()
        for seg in body.segments.values():
            for actor_id in seg.keys():
                all_new_actors.add(actor_id)
                
        # with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
        for actor_id in all_new_actors:
            if not db_data.exists(actor_id):
                return f'Actor {actor_id} does not exist', 404
                    
        # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock2:
        db_seg.json().set(pattern, Path.rootPath(), util.serialize(body))
        actors_segs = {}
        for seg_name, actors in body.segments.items():
            for actor_id, membership in actors.items():
                if actor_id not in actors_segs:
                    actors_segs[actor_id] = {}
                actors_segs[actor_id][seg_name] = membership
        for actor_id, segs in actors_segs.items():
            actor_seg_body = ActorSegmentCollection(
                provider_name=body.provider_name,
                collection_name=body.collection_name,
                version=body.version,
                segments=segs
            )
            db_data.json().set(actor_id, Path(
                f'segmentCollections["{pattern}"]'), util.serialize(actor_seg_body))
        return 'Created', 201
    return 'Bad request', 400


@util.generic_db_lock_decor
def segment_collection_validate_post(body, user=None, token_info=None):  # noqa: E501
    """segment_collection_validate_post

    Validate a new segment collection. # noqa: E501

    :param body: The new segment collection to add
    :type body: dict | bytes

    :rtype: List[str]
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), UiucSegmentCollection)  # noqa: E501
        pattern = util.get_collection_pattern(
            'actor', body.collection_name, body.provider_name, body.version)
        if pattern.find('*') != -1:
            return 'Bad request', 400
        
        db_data = util.get_db(db_name='actor_data')
        db_seg = util.get_db(db_name='segment')

        # with db_seg.lock('db_segment_lock', blocking_timeout=5) as lock1:
        if db_seg.exists(pattern):
            return 'Segment collection already exists', 409
        
        all_actors = set()
        for seg in body.segments.values():
            for actor_id in seg.keys():
                all_actors.add(actor_id)
        
        actor_list = []
        # with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
        for actor_id in all_actors:
            if not db_data.exists(actor_id):
                actor_list.append(actor_id)
        return actor_list, 200
    return 'Bad request', 400
