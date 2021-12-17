import connexion
import six

from swagger_server.models.actor_actor_graph import ActorActorGraph  # noqa: E501
from swagger_server.models.actor_message_graph import ActorMessageGraph  # noqa: E501
from swagger_server.models.message_message_graph import MessageMessageGraph  # noqa: E501
from swagger_server.models.uiuc_actor import UiucActor  # noqa: E501
from swagger_server.models.uiuc_message import UiucMessage  # noqa: E501
from swagger_server import util


def actor_actor_graph_get(provider_name, time_stamp, version=None):  # noqa: E501
    """actor_actor_graph_get

    Gets graph id by providerName, timestamp and version # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: str
    """
    return 'do some magic!'


def actor_actor_graph_id_delete(id, provider_name, time_stamp, version):  # noqa: E501
    """actor_actor_graph_id_delete

    Delete the specific graph by id, providerName, timestamp and version # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def actor_actor_graph_id_get(id, provider_name=None, time_stamp=None, version=None):  # noqa: E501
    """actor_actor_graph_id_get

    Gets specific actor-actor graph information by id, timeStamp, providerName and version # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: List[ActorActorGraph]
    """
    return 'do some magic!'


def actor_actor_graph_id_neighbor_get(id, provider_name, graph_type, version, actor_id):  # noqa: E501
    """actor_actor_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id, providerName and version and actor id # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param graph_type: 
    :type graph_type: str
    :param version: 
    :type version: str
    :param actor_id: 
    :type actor_id: str

    :rtype: List[List[UiucActor]]
    """
    return 'do some magic!'


def actor_actor_graph_id_put(body, provider_name, time_stamp, version, id):  # noqa: E501
    """actor_actor_graph_id_put

    Update the specific actor-actor graph by id, providerName, timestamp and version # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str
    :param id: Graph ID
    :type id: str

    :rtype: ActorActorGraph
    """
    if connexion.request.is_json:
        body = ActorActorGraph.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_actor_graph_post(body):  # noqa: E501
    """actor_actor_graph_post

    Creates new graphs # noqa: E501

    :param body: The new graphs to add
    :type body: list | bytes

    :rtype: List[ActorActorGraph]
    """
    if connexion.request.is_json:
        body = [ActorActorGraph.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def actor_message_graph_get(provider_name, time_stamp, version=None):  # noqa: E501
    """actor_message_graph_get

    Gets graph id by providerName, timestamp and version # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: str
    """
    return 'do some magic!'


def actor_message_graph_id_delete(id, provider_name, time_stamp, version):  # noqa: E501
    """actor_message_graph_id_delete

    Delete the specific graph by id, providerName, timestamp and version # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def actor_message_graph_id_get(id, provider_name=None, time_stamp=None, version=None):  # noqa: E501
    """actor_message_graph_id_get

    Gets specific actor-message graph information by id, timeStamp, providerName and version # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: List[ActorMessageGraph]
    """
    return 'do some magic!'


def actor_message_graph_id_neighbor_get(id, provider_name, graph_type, version, message_id=None, actor_id=None):  # noqa: E501
    """actor_message_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id, providerName and version and message or actor id # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param graph_type: 
    :type graph_type: str
    :param version: 
    :type version: str
    :param message_id: 
    :type message_id: str
    :param actor_id: 
    :type actor_id: str

    :rtype: List[List[Object]]
    """
    return 'do some magic!'


def actor_message_graph_id_put(body, provider_name, time_stamp, version, id):  # noqa: E501
    """actor_message_graph_id_put

    Update the specific actor-message graph by id, providerName, timestamp and version # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str
    :param id: Graph ID
    :type id: str

    :rtype: ActorMessageGraph
    """
    if connexion.request.is_json:
        body = ActorMessageGraph.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def actor_message_graph_post(body):  # noqa: E501
    """actor_message_graph_post

    Creates new graphs # noqa: E501

    :param body: The new graphs to add
    :type body: list | bytes

    :rtype: List[ActorMessageGraph]
    """
    if connexion.request.is_json:
        body = [ActorMessageGraph.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def message_message_graph_get(provider_name, time_stamp, version=None):  # noqa: E501
    """message_message_graph_get

    Gets graph id by providerName, timestamp and version # noqa: E501

    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: str
    """
    return 'do some magic!'


def message_message_graph_id_delete(id, provider_name, time_stamp, version):  # noqa: E501
    """message_message_graph_id_delete

    Delete the specific graph by id, providerName, timestamp and version # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: None
    """
    return 'do some magic!'


def message_message_graph_id_get(id, provider_name=None, time_stamp=None, version=None):  # noqa: E501
    """message_message_graph_id_get

    Gets specific message-message graph information by id, timeStamp, providerName and version # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str

    :rtype: List[MessageMessageGraph]
    """
    return 'do some magic!'


def message_message_graph_id_neighbor_get(id, provider_name, graph_type, version, message_id):  # noqa: E501
    """message_message_graph_id_neighbor_get

    Gets the neighbors for specific node from specific graph by graph id, providerName and version and message&#x27;s id # noqa: E501

    :param id: Graph ID
    :type id: str
    :param provider_name: 
    :type provider_name: str
    :param graph_type: 
    :type graph_type: str
    :param version: 
    :type version: str
    :param message_id: 
    :type message_id: str

    :rtype: List[List[UiucMessage]]
    """
    return 'do some magic!'


def message_message_graph_id_put(body, provider_name, time_stamp, version, id):  # noqa: E501
    """message_message_graph_id_put

    Update the specific message-message graph by id, providerName, timestamp and version # noqa: E501

    :param body: The new graph to update
    :type body: dict | bytes
    :param provider_name: 
    :type provider_name: str
    :param time_stamp: 
    :type time_stamp: str
    :param version: 
    :type version: str
    :param id: Graph ID
    :type id: str

    :rtype: MessageMessageGraph
    """
    if connexion.request.is_json:
        body = MessageMessageGraph.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def message_message_graph_post(body):  # noqa: E501
    """message_message_graph_post

    Creates new graphs # noqa: E501

    :param body: The new graphs to add
    :type body: list | bytes

    :rtype: List[MessageMessageGraph]
    """
    if connexion.request.is_json:
        body = [MessageMessageGraph.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
