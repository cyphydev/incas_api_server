import connexion
import six
import dpath.util

import redis
from redis.exceptions import LockError
from jsonpath_ng import jsonpath, parse
from redis.commands.json.path import Path

from uiuc_incas_server.models.actor_actor_graph import ActorActorGraph  # noqa: E501
from uiuc_incas_server.models.actor_actor_graph_db import ActorActorGraphDB  # noqa: E501
from uiuc_incas_server.models.actor_message_edge import ActorMessageEdge  # noqa: E501
from uiuc_incas_server.models.actor_message_graph import ActorMessageGraph  # noqa: E501
from uiuc_incas_server.models.actor_message_graph_db import ActorMessageGraphDB  # noqa: E501
from uiuc_incas_server.models.actor_to_actor_edge import ActorToActorEdge  # noqa: E501
from uiuc_incas_server.models.message_message_graph import MessageMessageGraph  # noqa: E501
from uiuc_incas_server.models.message_message_graph_db import MessageMessageGraphDB  # noqa: E501
from uiuc_incas_server.models.message_to_message_edge import MessageToMessageEdge  # noqa: E501
from uiuc_incas_server import util

get_db = connexion.utils.get_function_from_name('uiuc_incas_server.util.get_db')

def actor_actor_graph_get(provider_name, time_stamp, version):  # noqa: E501
    """actor_actor_graph_get

    Gets graph id by providerName, timestamp and version. # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: str
    """
    pattern = f'actor_actor:{provider_name}:{time_stamp}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if not db_meta.exists(pattern):
                return 'Graph does not exist', 404
            graph_id = db_meta.json().get(pattern, Path.rootPath())
            return graph_id, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_actor_graph_id_delete(id_):  # noqa: E501
    """actor_actor_graph_id_delete

    Delete the specific graph by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            db_graph.delete(id_, Path.rootPath())
            return 'Deleted', 204
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_actor_graph_id_get(id_):  # noqa: E501
    """actor_actor_graph_id_get

    Gets specific actor-actor graph information by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: ActorActorGraph
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            record = db_graph.json().get(id_, Path.rootPath())
        record['edges'] = list(record['edges'].values())
        ret = util.deserialize(record, ActorActorGraph)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_actor_graph_id_neighbor_get(id_, actor_id):  # noqa: E501
    """actor_actor_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id and actor id. # noqa: E501

    :param id: Graph ID
    :type id: str
    :param actor_id: 
    :type actor_id: str

    :rtype: List[ActorToActorEdge]
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            edges = db_graph.json().get(id_, Path(f'edges'))
        ret = dpath.util.values(edges, f'{actor_id}-*-*')
        ret = util.serialize(ret)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_actor_graph_id_put(body, id_):  # noqa: E501
    """actor_actor_graph_id_put

    Update the specific actor-actor graph by id. # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorActorGraph)  # noqa: E501
        db_graph = get_db(db_name='graph')
        try:
            with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
                if not db_graph.exists(id_):
                    return 'Key does not exist', 404

                content = util.serialize(body)
                content['edges'] = {f'{edge["actorId1"]}-{edge["actorId2"]}-{edge["edgeId"]}': edge for edge in content['edges']}
                content = util.deserialize(content, ActorActorGraphDB)

                db_graph.json().set(id_, Path.rootPath(), util.serialize(content))
                return 'Updated', 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_actor_graph_post(body):  # noqa: E501
    """actor_actor_graph_post

    Submits a new graph. # noqa: E501

    :param body: The new graphs to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorActorGraph)  # noqa: E501
        pattern = f'actor_actor:{body.provider_name}:{body.time_stamp}:{body.version}'
        db_meta = get_db(db_name='meta')
        db_graph = get_db(db_name='graph')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock1:
                with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock2:
                    if db_meta.exists(pattern):
                        return 'Graph already exists', 409
                    
                    content = util.serialize(body)
                    content['edges'] = {f'{edge["actorId1"]}-{edge["actorId2"]}-{edge["edgeId"]}': edge for edge in content['edges']}
                    content = util.deserialize(content, ActorActorGraphDB)

                    graph_id = pattern
                    db_meta.json().set(pattern, Path.rootPath(), graph_id)
                    db_graph.json().set(graph_id, Path.rootPath(), util.serialize(content))
                    return 'Created', 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_message_graph_get(provider_name, time_stamp, version):  # noqa: E501
    """actor_message_graph_get

    Gets graph id by providerName, timestamp and version. # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: str
    """
    pattern = f'actor_message:{provider_name}:{time_stamp}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if not db_meta.exists(pattern):
                return 'Graph does not exist', 404
            graph_id = db_meta.json().get(pattern, Path.rootPath())
            return graph_id, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_message_graph_id_delete(id_):  # noqa: E501
    """actor_message_graph_id_delete

    Delete the specific graph by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            db_graph.delete(id_, Path.rootPath())
            return 'Deleted', 204
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_message_graph_id_get(id_):  # noqa: E501
    """actor_message_graph_id_get

    Gets specific actor-message graph information by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: ActorMessageGraph
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            record = db_graph.json().get(id_, Path.rootPath())
        record['edges'] = list(record['edges'].values())
        ret = util.deserialize(record, ActorMessageGraph)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_message_graph_id_neighbor_get(id_, message_id=None, actor_id=None):  # noqa: E501
    """actor_message_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id and message or actor id. # noqa: E501

    :param id: Graph ID
    :type id: str
    :param message_id: 
    :type message_id: str
    :param actor_id: 
    :type actor_id: str

    :rtype: List[ActorMessageEdge]
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            edges = db_graph.json().get(id_, Path(f'edges'))
        # check if current node is actor or message
        res = None 
        if actor_id is not None:
            ret = dpath.util.values(edges, f'{actor_id}-*-*')
        elif message_id is not None:
            ret = dpath.util.values(edges, f'{message_id}-*-*')
        else:
            return 'Bad request', 400
        ret = util.serialize(ret)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_message_graph_id_put(body, id_):  # noqa: E501
    """actor_message_graph_id_put

    Update the specific actor-message graph by id. # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorMessageGraph)  # noqa: E501
        db_graph = get_db(db_name='graph')
        try:
            with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
                if not db_graph.exists(id_):
                    return 'Key does not exist', 404

                content = util.serialize(body)
                edges = {}
                for i in range(len(content['edges'])):
                    edge = content['edges'][i]
                    if edge['edgeType'] == 'actor_message':
                        edges[f'{edge["actorId"]}-{edge["messageId"]}-{edge["edgeId"]}'] = edge
                    elif edge['edgeType'] == 'message_actor':
                        edges[f'{edge["messageId"]}-{edge["actorId"]}-{edge["edgeId"]}'] = edge
                    else:
                        return 'Bad request', 400
                content['edges'] = edges
                content = util.deserialize(content, ActorMessageGraphDB)

                db_graph.json().set(id_, Path.rootPath(), util.serialize(content))
                return 'Updated', 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def actor_message_graph_post(body):  # noqa: E501
    """actor_message_graph_post

    Submits a new graph. # noqa: E501

    :param body: The new graphs to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), ActorMessageGraph)  # noqa: E501
        pattern = f'actor_message:{body.provider_name}:{body.time_stamp}:{body.version}'
        db_meta = get_db(db_name='meta')
        db_graph = get_db(db_name='graph')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock1:
                with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock2:
                    if db_meta.exists(pattern):
                        return 'Graph already exists', 409
                    
                    content = util.serialize(body)
                    edges = {}
                    for i in range(len(content['edges'])):
                        edge = content['edges'][i]
                        if edge['edgeType'] == 'actor_message':
                            edges[f'{edge["actorId"]}-{edge["messageId"]}-{edge["edgeId"]}'] = edge
                        elif edge['edgeType'] == 'message_actor':
                            edges[f'{edge["messageId"]}-{edge["actorId"]}-{edge["edgeId"]}'] = edge
                        else:
                            return 'Bad request', 400
                    content['edges'] = edges
                    content = util.deserialize(content, ActorMessageGraphDB)

                    graph_id = pattern
                    db_meta.json().set(pattern, Path.rootPath(), graph_id)
                    db_graph.json().set(graph_id, Path.rootPath(), util.serialize(content))
                    return 'Created', 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def message_message_graph_get(provider_name, time_stamp, version):  # noqa: E501
    """message_message_graph_get

    Gets graph id by providerName, timestamp and version. # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: str
    """
    pattern = f'message_message:{provider_name}:{time_stamp}:{version}'
    db_meta = get_db(db_name='meta')
    try:
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if not db_meta.exists(pattern):
                return 'Graph does not exist', 404
            message_id = db_meta.json().get(pattern, Path.rootPath())
            return message_id, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def message_message_graph_id_delete(id_):  # noqa: E501
    """message_message_graph_id_delete

    Delete the specific graph by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            db_graph.delete(id_, Path.rootPath())
            return 'Deleted', 204
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def message_message_graph_id_get(id_):  # noqa: E501
    """message_message_graph_id_get

    Gets specific message-message graph information by id. # noqa: E501

    :param id: Graph ID
    :type id: str

    :rtype: MessageMessageGraph
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            record = db_graph.json().get(id_, Path.rootPath())
        record['edges'] = list(record['edges'].values())
        ret = util.deserialize(record, MessageMessageGraph)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def message_message_graph_id_neighbor_get(id_, message_id):  # noqa: E501
    """message_message_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id and message&#x27;s id. # noqa: E501

    :param id: Graph ID
    :type id: str
    :param message_id: 
    :type message_id: str

    :rtype: List[MessageToMessageEdge]
    """
    db_graph = get_db(db_name='graph')
    try:
        with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
            if not db_graph.exists(id_):
                return 'Key does not exist', 404
            edges = db_graph.json().get(id_, Path(f'edges'))
        ret = dpath.util.values(edges, f'{message_id}-*-*')
        ret = util.serialize(ret)
        return ret, 200
    except LockError:
        return 'Lock not acquired', 500
    return 'Bad request', 400


def message_message_graph_id_put(body, id_):  # noqa: E501
    """message_message_graph_id_put

    Update the specific message-message graph by id. # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param id: Graph ID
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageMessageGraph)  # noqa: E501
        db_graph = get_db(db_name='graph')
        try:
            with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock:
                if not db_graph.exists(id_):
                    return 'Key does not exist', 404

                content = util.serialize(body)
                content['edges'] = {f'{edge["messageId1"]}-{edge["messageId2"]}-{edge["edgeId"]}': edge for edge in content['edges']}
                content = util.deserialize(content, MessageMessageGraphDB)

                db_graph.json().set(id_, Path.rootPath(), util.serialize(content))
                return 'Updated', 200
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400


def message_message_graph_post(body):  # noqa: E501
    """message_message_graph_post

    Submits a new graph. # noqa: E501

    :param body: The new graph to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = util.deserialize(connexion.request.get_json(), MessageMessageGraph)  # noqa: E501
        pattern = f'message_message:{body.provider_name}:{body.time_stamp}:{body.version}'
        db_meta = get_db(db_name='meta')
        db_graph = get_db(db_name='graph')
        try:
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock1:
                with db_graph.lock('db_graph_lock', blocking_timeout=5) as lock2:
                    if db_meta.exists(pattern):
                        return 'Graph already exists', 409
                    
                    content = util.serialize(body)
                    content['edges'] = {f'{edge["messageId1"]}-{edge["messageId2"]}-{edge["edgeId"]}': edge for edge in content['edges']}
                    content = util.deserialize(content, MessageMessageGraphDB)

                    graph_id = pattern
                    db_meta.json().set(pattern, Path.rootPath(), graph_id)
                    db_graph.json().set(graph_id, Path.rootPath(), util.serialize(content))
                    return 'Created', 201
        except LockError:
            return 'Lock not acquired', 500
    return 'Bad request', 400
