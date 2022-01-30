import connexion
import six
import dpath.util

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.actor_actor_graph import ActorActorGraph  # noqa: E501
from uiuc_incas_server.models.actor_actor_graph_db import ActorActorGraphDB  # noqa: E501
from uiuc_incas_server.models.actor_message_graph import ActorMessageGraph  # noqa: E501
from uiuc_incas_server.models.actor_message_graph_db import ActorMessageGraphDB  # noqa: E501
from uiuc_incas_server.models.graph_edge import GraphEdge  # noqa: E501
from uiuc_incas_server.models.message_message_graph import MessageMessageGraph  # noqa: E501
from uiuc_incas_server.models.message_message_graph_db import MessageMessageGraphDB  # noqa: E501
from uiuc_incas_server import util

def generic_graph_list_get(prefix, provider_name, graph_name, distance_name, version, time_stamp, return_code=200):
    pattern = util.get_graph_pattern(prefix, provider_name, graph_name, distance_name, version, time_stamp)
    
    if pattern.find('*') != -1:
        return "Bad request", 400

    db_meta = util.get_db(db_name='meta')
    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        graph_ids = list(util.get_all_keys(db_meta, pattern))
    return graph_ids, return_code

def generic_graph_id_neighbor_get(id_, src_id, return_code=200):
    db_graph = util.get_db(db_name='graph')

    with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
        if not db_graph.exists(id_):
            return 'Key does not exist', 404
        edges = db_graph.json().get(id_, Path(f'edges'))

    ret = dpath.util.values(edges, f'{src_id}:*:*')
    ret = util.serialize(ret)
    return ret, return_code

def generic_graph_id_get(id_, klass, return_code=200):
    db_graph = util.get_db(db_name='graph')

    with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
        if not db_graph.exists(id_):
            return 'Key does not exist', 404
        record = db_graph.json().get(id_, Path.rootPath())
    record['edges'] = list(record['edges'].values())
    ret = util.deserialize(record, klass)
    return ret, return_code

def generic_graph_post(body, pattern, klass, return_code=201):
    db_meta = util.get_db(db_name='meta')
    db_graph = util.get_db(db_name='graph')

    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock_meta:
        if db_meta.exists(pattern):
            return 'Graph already exists', 409

    if pattern.find('*') != -1:
        return "Bad request", 400

    content = util.serialize(body)
    content['edges'] = {f'{edge["srcId"]}:{edge["dstId"]}:{edge["actionType"]}': edge for edge in content['edges']}
    content = util.deserialize(content, klass)
    graph_id = pattern

    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock1:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock2:
            db_meta.json().set(pattern, Path.rootPath(), graph_id)
            db_graph.json().set(graph_id, Path.rootPath(), util.serialize(content))
    return 'Created', return_code

def generic_graph_id_put(prefix, id_, body, klass, return_code=200):
    if id_ != f'{prefix}:{body.provider_name}:{body.graph_name}:{body.distance_name}:{body.version}:{body.time_stamp}':
        return "Graph ID and its realted fields are not changeable", 400

    db_graph = util.get_db(db_name='graph')

    with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
        if not db_graph.exists(id_):
            return 'Key does not exist', 404

    content = util.serialize(body)
    content['edges'] = {f'{edge["srcId"]}:{edge["dstId"]}:{edge["actionType"]}': edge for edge in content['edges']}
    content = util.deserialize(content, klass)

    with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
        db_graph.json().set(id_, Path.rootPath(), util.serialize(content))
    return 'Updated', return_code

def generic_graph_id_delete(id_, return_code=204):
    db_meta = util.get_db(db_name='meta')
    db_graph = util.get_db(db_name='graph')

    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        if not db_meta.exists(id_): 
            return 'Key does not exist in the meta database', 404
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_): 
                return 'Key does not exist in the graph database', 404
            db_meta.delete(id_, Path.rootPath())
            db_graph.delete(id_, Path.rootPath())

    return 'Deleted', return_code


@util.generic_db_lock_decor
def actor_actor_graph_id_delete(id_, user=None, token_info=None):  # noqa: E501
    """actor_actor_graph_id_delete

    Delete the specific graph by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    return generic_graph_id_delete(id_)


@util.generic_db_lock_decor
def actor_actor_graph_id_get(id_, user=None, token_info=None):  # noqa: E501
    """actor_actor_graph_id_get

    Gets specific actor-actor graph information by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: ActorActorGraph
    """
    return generic_graph_id_get(id_, ActorActorGraph)


@util.generic_db_lock_decor
def actor_actor_graph_id_neighbor_get(id_, actor_id, user=None, token_info=None):  # noqa: E501
    """actor_actor_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id and actor id. # noqa: E501

    :param id: Graph ID
    :type id: str
    :param actor_id: 
    :type actor_id: str

    :rtype: List[GraphEdge]
    """
    return generic_graph_id_neighbor_get(id_, actor_id)


@util.generic_db_lock_decor
def actor_actor_graph_id_put(body, id_, user=None, token_info=None):  # noqa: E501
    """actor_actor_graph_id_put

    Update the specific actor-actor graph by id. # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param id: Graph ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorActorGraph)  # noqa: E501
        return generic_graph_id_put('actor_actor', id_, body, ActorActorGraphDB)
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_actor_graph_list_get(provider_name=None, graph_name=None, distance_name=None, version=None, time_stamp=None, user=None, token_info=None):  # noqa: E501
    """actor_actor_graph_list_get

    Gets graph IDs by providing query keys. # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param graph_name: 
    :type graph_name: str
    :param distance_name: 
    :type distance_name: str
    :param version: 
    :type version: str
    :param time_stamp: 
    :type time_stamp: str

    :rtype: List[str]
    """
    return generic_graph_list_get('actor_actor', provider_name, graph_name, distance_name, version, time_stamp)


@util.generic_db_lock_decor
def actor_actor_graph_post(body, user=None, token_info=None):  # noqa: E501
    """actor_actor_graph_post

    Submits a new graph. # noqa: E501

    :param body: The new graphs to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorActorGraph)  # noqa: E501
        pattern = util.get_graph_pattern('actor_actor', body.provider_name, body.graph_name, body.distance_name, body.version, body.time_stamp)
        return generic_graph_post(body, pattern, ActorActorGraphDB)
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_message_graph_id_delete(id_, user=None, token_info=None):  # noqa: E501
    """actor_message_graph_id_delete

    Delete the specific graph by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    return generic_graph_id_delete(id_)


@util.generic_db_lock_decor
def actor_message_graph_id_get(id_, user=None, token_info=None):  # noqa: E501
    """actor_message_graph_id_get

    Gets specific actor-message graph information by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: ActorMessageGraph
    """
    return generic_graph_id_get(id_, ActorMessageGraph)


@util.generic_db_lock_decor
def actor_message_graph_id_neighbor_get(id_, message_id=None, actor_id=None, user=None, token_info=None):  # noqa: E501
    """actor_message_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id and message or actor id. # noqa: E501

    :param id: Graph ID
    :type id: str
    :param message_id: 
    :type message_id: str
    :param actor_id: 
    :type actor_id: str

    :rtype: List[GraphEdge]
    """
    if message_id is not None and actor_id is not None:
        return 'Bad request', 400
    elif message_id is not None:
        return generic_graph_id_neighbor_get(id_, message_id)
    elif actor_id is not None:
        return generic_graph_id_neighbor_get(id_, actor_id)
    else:
        return 'Bad request', 400


@util.generic_db_lock_decor
def actor_message_graph_id_put(body, id_, user=None, token_info=None):  # noqa: E501
    """actor_message_graph_id_put

    Update the specific actor-message graph by id. # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param id: Graph ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorMessageGraph)  # noqa: E501
        return generic_graph_id_put('actor_message', id_, body, ActorMessageGraphDB)
    return 'Bad request', 400


@util.generic_db_lock_decor
def actor_message_graph_list_get(provider_name=None, graph_name=None, distance_name=None, version=None, time_stamp=None, user=None, token_info=None):  # noqa: E501
    """actor_message_graph_list_get

    Gets graph IDs by providing query keys. # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param graph_name: 
    :type graph_name: str
    :param distance_name: 
    :type distance_name: str
    :param version: 
    :type version: str
    :param time_stamp: 
    :type time_stamp: str

    :rtype: List[str]
    """
    return generic_graph_list_get('actor_message', provider_name, graph_name, distance_name, version, time_stamp)


@util.generic_db_lock_decor
def actor_message_graph_post(body, user=None, token_info=None):  # noqa: E501
    """actor_message_graph_post

    Submits a new graph. # noqa: E501

    :param body: The new graphs to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorMessageGraph)  # noqa: E501
        pattern = util.get_graph_pattern('actor_message', body.provider_name, body.graph_name, body.distance_name, body.version, body.time_stamp)
        return generic_graph_post(body, pattern, ActorMessageGraphDB)
    return 'Bad request', 400


@util.generic_db_lock_decor
def message_message_graph_id_delete(id_, user=None, token_info=None):  # noqa: E501
    """message_message_graph_id_delete

    Delete the specific graph by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    return generic_graph_id_delete(id_)


@util.generic_db_lock_decor
def message_message_graph_id_get(id_, user=None, token_info=None):  # noqa: E501
    """message_message_graph_id_get

    Gets specific message-message graph information by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: MessageMessageGraph
    """
    return generic_graph_id_get(id_, MessageMessageGraph)


@util.generic_db_lock_decor
def message_message_graph_id_neighbor_get(id_, message_id, user=None, token_info=None):  # noqa: E501
    """message_message_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id and message&#x27;s id. # noqa: E501

    :param id: Graph ID
    :type id: str
    :param message_id: 
    :type message_id: str

    :rtype: List[GraphEdge]
    """
    return generic_graph_id_neighbor_get(id_, message_id)


@util.generic_db_lock_decor
def message_message_graph_id_put(body, id_, user=None, token_info=None):  # noqa: E501
    """message_message_graph_id_put

    Update the specific message-message graph by id. # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param id: Graph ID
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageMessageGraph)  # noqa: E501
        return generic_graph_id_put('message_message', id_, body, MessageMessageGraphDB)
    return 'Bad request', 400


@util.generic_db_lock_decor
def message_message_graph_list_get(provider_name=None, graph_name=None, distance_name=None, version=None, time_stamp=None, user=None, token_info=None):  # noqa: E501
    """message_message_graph_list_get

    Gets graph IDs by providing query keys. # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param graph_name: 
    :type graph_name: str
    :param distance_name: 
    :type distance_name: str
    :param version: 
    :type version: str
    :param time_stamp: 
    :type time_stamp: str

    :rtype: List[str]
    """
    return generic_graph_list_get('message_message', provider_name, graph_name, distance_name, version, time_stamp)


@util.generic_db_lock_decor
def message_message_graph_post(body, user=None, token_info=None):  # noqa: E501
    """message_message_graph_post

    Submits a new graph. # noqa: E501

    :param body: The new graph to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageMessageGraph)  # noqa: E501
        pattern = util.get_graph_pattern('message_message', body.provider_name, body.graph_name, body.distance_name, body.version, body.time_stamp)
        return generic_graph_post(body, pattern, ActorActorGraphDB)
    return 'Bad request', 400
