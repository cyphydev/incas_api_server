import connexion
from connexion.exceptions import OAuthProblem
import six

import redis
from redis.exceptions import LockError
from redis.commands.json.path import Path

from uiuc_incas_server.models.actor_id_response import ActorIdResponse  # noqa: E501
from uiuc_incas_server.models.message_id_response import MessageIdResponse  # noqa: E501
from uiuc_incas_server.models.uiuc_actor import UiucActor  # noqa: E501
from uiuc_incas_server.models.uiuc_actor_db import UiucActorDB  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server.models.uiuc_message_db import UiucMessageDB  # noqa: E501
from uiuc_incas_server import util


@util.generic_db_lock_decor
def admin_actor_post(body, user=None, token_info=None):  # noqa: E501
    """admin_actor_post

    Add actors. # noqa: E501

    :param body: Array of actors
    :type body: list | bytes

    :rtype: str
    """
    if 'scope' not in token_info or 'admin' not in token_info['scope']:
        raise OAuthProblem('Not authorized')
    if connexion.request.is_json:
        bodies = [util.serialize(util.deserialize(d, UiucActor)) for d in connexion.request.get_json()]  # noqa: E501
        for actor in bodies:
            if actor['uiucMediaType'] is None or actor['uiucMediaType'] == '':
                return 'Media type cannot be empty', 400
            if actor['entityType'] is None or actor['entityType'] == '':
                return 'Entity type cannot be empty', 400

        db_idx = util.get_db(db_name='index')
        db_meta = util.get_db(db_name='meta')
        db_data = util.get_db(db_name='actor_data')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if not db_meta.exists('status'):
                db_meta.json().set('status', Path.rootPath(), {})

        with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
            # for actor in bodies:
            #     data_pattern = f'actor:{actor["mediaType"].lower()}:{actor["entityType"].lower()}:{actor["id"]}'
            #     if db_data.exists(data_pattern):
            #         return f'Actor {data_pattern} already exists', 409
            
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock2:
                with db_idx.lock('db_index_lock', blocking_timeout=5) as lock3:
                    for actor in bodies:
                        actor['enrichments'] = {}
                        actor['segmentCollections'] = {}
                        idx_pattern = f'forward:actor:{actor["uiucMediaType"].lower()}:{actor["entityType"].lower()}'
                        idx_pattern_status = idx_pattern.replace(':', '_')
                        data_pattern = f'actor:{actor["uiucMediaType"].lower()}:{actor["entityType"].lower()}:{actor["id"]}'
                        rev_idx_pattern = f'reverse:{data_pattern}'
                        actor['uiucAuthorId'] = data_pattern

                        if db_meta.json().type('status', Path(idx_pattern_status)) is None:
                            db_meta.json().set('status', Path(idx_pattern_status), util.count_keys(db_idx, idx_pattern + ':*'))
                        counter = db_meta.json().get('status', Path(idx_pattern_status))

                        db_idx.json().set(idx_pattern + f':{counter}', Path.rootPath(), util.serialize(ActorIdResponse(
                            global_id=actor['id'],
                            actor_id=data_pattern
                        )))
                        db_idx.json().set(rev_idx_pattern, Path.rootPath(), idx_pattern + f':{counter}')

                        db_data.json().set(data_pattern, Path.rootPath(), actor)
                        db_meta.json().set('status', Path(idx_pattern_status), counter + 1)
        return 'OK', 201
    return 'Bad Request', 400


@util.generic_db_lock_decor
def admin_message_post(body, user=None, token_info=None):  # noqa: E501
    """admin_message_post

    Add messages. # noqa: E501

    :param body: Array of messages
    :type body: list | bytes

    :rtype: str
    """
    if 'scope' not in token_info or 'admin' not in token_info['scope']:
        raise OAuthProblem('Not authorized')
    if connexion.request.is_json:
        bodies = [util.serialize(util.deserialize(d, UiucMessage)) for d in connexion.request.get_json()]  # noqa: E501
        for message in bodies:
            if message['mediaType'] is None or message['mediaType'] == '':
                return 'Media type cannot be empty', 400

        db_idx = util.get_db(db_name='index')
        db_meta = util.get_db(db_name='meta')
        db_data = util.get_db(db_name='message_data')
        with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
            if not db_meta.exists('status'):
                db_meta.json().set('status', Path.rootPath(), {})

        with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock1:
            # for message in bodies:
            #     data_pattern = f'message:{message["mediaType"].lower()}:{message["id"]}'
            #     if db_data.exists(data_pattern):
            #         return f'Message {data_pattern} already exists', 409
            
            with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock2:
                with db_idx.lock('db_index_lock', blocking_timeout=5) as lock3:
                    for message in bodies:
                        message['enrichments'] = {}
                        idx_pattern = f'forward:message:{message["mediaType"].lower()}'
                        idx_pattern_status = idx_pattern.replace(':', '_')
                        if message["mediaType"].lower() == 'twitter':
                            data_pattern = f'message:{message["mediaType"].lower()}:{message["mediaTypeAttributes"]["twitterData"]["tweetId"]}'
                        else:
                            return 'Unsupported media type', 400
                        rev_idx_pattern = f'reverse:{data_pattern}'
                        message['uiucMessageId'] = data_pattern

                        if db_meta.json().type('status', Path(idx_pattern_status)) is None:
                            db_meta.json().set('status', Path(idx_pattern_status), util.count_keys(db_idx, idx_pattern + ':*'))
                        counter = db_meta.json().get('status', Path(idx_pattern_status))

                        db_idx.json().set(idx_pattern + f':{counter}', Path.rootPath(), util.serialize(MessageIdResponse(
                            global_id=message['id'],
                            media_id=data_pattern
                        )))
                        db_idx.json().set(rev_idx_pattern, Path.rootPath(), idx_pattern + f':{counter}')

                        db_data.json().set(data_pattern, Path.rootPath(), message)
                        db_meta.json().set('status', Path(idx_pattern_status), counter + 1)
        return 'OK', 201
    return 'Bad Request', 400
