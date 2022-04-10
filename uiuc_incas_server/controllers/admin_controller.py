import connexion
from connexion.exceptions import OAuthProblem
import six
import logging

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
        # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        if not db_meta.exists('status'):
            db_meta.json().set('status', Path.root_path(), {})

        # with db_data.lock('db_actor_data_lock', blocking_timeout=5) as lock1:
        filtered_bodies = []
        exist_bodies = []
        for actor in bodies:
            data_pattern = f'actor:{actor["uiucMediaType"].lower()}:{actor["entityType"].lower()}:{actor["id"]}'
            rev_idx_pattern = f'reverse:{data_pattern}'
            e_a, e_b, e_c = db_data.exists(data_pattern), db_idx.exists(rev_idx_pattern), False
            if e_b:
                e_c = db_idx.exists(db_idx.json().get(rev_idx_pattern, Path.root_path()))
            if e_a and e_b and e_c:
                # logging.warning(f'Actor {data_pattern} already exists')
                exist_bodies.append(actor)
            elif not e_a and not e_b and not e_c:
                filtered_bodies.append(actor)
            else:
                return f'Actor DB is inconsistent.', 500
        
        # Update actors that exist
        for actor in exist_bodies:
            data_pattern = f'actor:{actor["uiucMediaType"].lower()}:{actor["entityType"].lower()}:{actor["id"]}'
            old_actor = db_data.json().get(data_pattern, Path.root_path())
            actor['enrichments'] = old_actor['enrichments'] if 'enrichments' in old_actor else {}
            actor['segmentCollections'] = old_actor['segmentCollections'] if 'segmentCollections' in old_actor else {}
            db_data.json().set(data_pattern, Path.root_path(), actor)

        #    with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock2:
        #        with db_idx.lock('db_index_lock', blocking_timeout=5) as lock3:
        for actor in filtered_bodies:
            actor['enrichments'] = {}
            actor['segmentCollections'] = {}
            idx_pattern = f'forward:actor:{actor["uiucMediaType"].lower()}:{actor["entityType"].lower()}'
            idx_pattern_status = idx_pattern.replace(':', '_')
            data_pattern = f'actor:{actor["uiucMediaType"].lower()}:{actor["entityType"].lower()}:{actor["id"]}'
            rev_idx_pattern = f'reverse:{data_pattern}'
            actor['uiucActorId'] = data_pattern

            if db_meta.json().type('status', Path(idx_pattern_status)) is None:
                db_meta.json().set('status', Path(idx_pattern_status), util.count_keys(db_idx, idx_pattern + ':*'))
            counter = db_meta.json().get('status', Path(idx_pattern_status))

            db_idx.json().set(idx_pattern + f':{counter}', Path.root_path(), util.serialize(ActorIdResponse(
                global_id=actor['id'],
                actor_id=data_pattern
            )))
            db_idx.json().set(rev_idx_pattern, Path.root_path(), idx_pattern + f':{counter}')

            db_data.json().set(data_pattern, Path.root_path(), actor)
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
        # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock:
        if not db_meta.exists('status'):
            db_meta.json().set('status', Path.root_path(), {})

        # with db_data.lock('db_message_data_lock', blocking_timeout=5) as lock1:
        filtered_bodies = []
        exist_bodies = []
        for message in bodies:
            if message["mediaType"].lower() == 'twitter':
                data_pattern = f'message:{message["mediaType"].lower()}:{message["mediaTypeAttributes"]["twitterData"]["tweetId"]}'
            else:
                return 'Unsupported media type', 400
            rev_idx_pattern = f'reverse:{data_pattern}'
            e_a, e_b, e_c = db_data.exists(data_pattern), db_idx.exists(rev_idx_pattern), False
            if e_b:
                e_c = db_idx.exists(db_idx.json().get(rev_idx_pattern, Path.root_path()))
            if e_a and e_b and e_c:
                # logging.warning(f'Message {data_pattern} already exists')
                exist_bodies.append(message)
            elif not e_a and not e_b and not e_c:
                filtered_bodies.append(message)
            else:
                return f'Message DB is inconsistent.', 500
        
        # Update messages that exist
        for message in exist_bodies:
            data_pattern = f'message:{message["mediaType"].lower()}:{message["mediaTypeAttributes"]["twitterData"]["tweetId"]}'
            old_message = db_data.json().get(data_pattern, Path.root_path())
            message['enrichments'] = old_message['enrichments'] if 'enrichments' in old_message else {}
            db_data.json().set(data_pattern, Path.root_path(), message)

            # with db_meta.lock('db_meta_lock', blocking_timeout=5) as lock2:
                # with db_idx.lock('db_index_lock', blocking_timeout=5) as lock3:
        for message in filtered_bodies:
            message['enrichments'] = {}
            idx_pattern = f'forward:message:{message["mediaType"].lower()}'
            idx_pattern_status = idx_pattern.replace(':', '_')
            data_pattern = f'message:{message["mediaType"].lower()}:{message["mediaTypeAttributes"]["twitterData"]["tweetId"]}'
            rev_idx_pattern = f'reverse:{data_pattern}'
            message['uiucMessageId'] = data_pattern

            if db_meta.json().type('status', Path(idx_pattern_status)) is None:
                db_meta.json().set('status', Path(idx_pattern_status), util.count_keys(db_idx, idx_pattern + ':*'))
            counter = db_meta.json().get('status', Path(idx_pattern_status))

            db_idx.json().set(idx_pattern + f':{counter}', Path.root_path(), util.serialize(MessageIdResponse(
                global_id=message['id'],
                media_id=data_pattern
            )))
            db_idx.json().set(rev_idx_pattern, Path.root_path(), idx_pattern + f':{counter}')

            db_data.json().set(data_pattern, Path.root_path(), message)
            db_meta.json().set('status', Path(idx_pattern_status), counter + 1)
        return 'OK', 201
    return 'Bad Request', 400
