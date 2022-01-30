from __future__ import absolute_import

import datetime
import json
import mimetypes
from multiprocessing.pool import ThreadPool
import os
import re
import tempfile

# python 2 and python 3 compatibility library
import six
from six.moves.urllib.parse import quote

from uiuc_incas_server import type_util
import uiuc_incas_server.models

import redis
from redis.exceptions import LockError

PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types
NATIVE_TYPES_MAPPING = {
    'int': int,
    'long': int if six.PY3 else long,  # noqa: F821
    'float': float,
    'str': str,
    'bool': bool,
    'date': datetime.date,
    'datetime': datetime.datetime,
    'object': object,
}

DB_IDX = {
    'index': 0,
    'auth': 1,
    'message_data': 2,
    'actor_data': 3,
    'meta': 4,
    'graph': 5,
    'segment': 6
}

DB_MAP = {
    'index': None,
    'auth': None,
    'message_data': None,
    'actor_data': None,
    'meta': None, # [message|actor]:name:provider:version -> EnrichmentMeta
                  # graph:provider:timestamp:version -> graph ID
    'graph': None,
    'segment': None
}

def get_db(db_name, server_host='localhost', server_port=6379):
    global DB_MAP
    if DB_MAP[db_name] is None:
        DB_MAP[db_name] = redis.Redis(server_host, server_port, DB_IDX[db_name])
    return DB_MAP[db_name]

def count_keys(db, pattern):
    cnt, cur = 0, 0
    cur, ks = db.execute_command(f'SCAN {cur} MATCH {pattern} COUNT 10000')
    cur = int(cur)
    cnt += len(ks)
    while cur != 0:
        cur, ks = db.execute_command(f'SCAN {cur} MATCH {pattern} COUNT 10000')
        cur = int(cur)
        cnt += len(ks)
    return cnt

def get_all_keys(db, pattern):
    cur, kks = 0, []
    cur, ks = db.execute_command(f'SCAN {cur} MATCH {pattern} COUNT 10000')
    cur = int(cur)
    kks.extend(map(lambda x: x.decode('utf-8'), ks))
    while cur != 0:
        cur, ks = db.execute_command(f'SCAN {cur} MATCH {pattern} COUNT 10000')
        cur = int(cur)
        kks.extend(map(lambda x: x.decode('utf-8'), ks))
    return set(kks)

def generic_db_lock_decor(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LockError:
            return 'Lock not acquired', 500
    return wrapper

def serialize(obj):
    return sanitize_for_serialization(obj)

def sanitize_for_serialization(obj):
    """Builds a JSON POST object.

    If obj is None, return None.
    If obj is str, int, long, float, bool, return directly.
    If obj is datetime.datetime, datetime.date
        convert to string in iso8601 format.
    If obj is list, sanitize each element in the list.
    If obj is dict, return the dict.
    If obj is swagger model, return the properties dict.

    :param obj: The data to serialize.
    :return: The serialized form of data.
    """
    if obj is None:
        return None
    elif isinstance(obj, PRIMITIVE_TYPES):
        return obj
    elif isinstance(obj, list):
        return [sanitize_for_serialization(sub_obj)
                for sub_obj in obj]
    elif isinstance(obj, tuple):
        return tuple(sanitize_for_serialization(sub_obj)
                        for sub_obj in obj)
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()

    if isinstance(obj, dict):
        obj_dict = obj
    else:
        # Convert model obj to dict except
        # attributes `swagger_types`, `attribute_map`
        # and attributes which value is not None.
        # Convert attribute name to json key in
        # model definition for request.
        obj_dict = {obj.attribute_map[attr]: getattr(obj, attr)
                    for attr, _ in six.iteritems(obj.swagger_types)
                    if getattr(obj, attr) is not None}

    return {key: sanitize_for_serialization(val)
            for key, val in six.iteritems(obj_dict)}

def deserialize(response, response_type):
    """Deserializes response into an object.

    :param response: RESTResponse object to be deserialized.
    :param response_type: class literal for
        deserialized object, or string of class name.

    :return: deserialized object.
    """

    return __deserialize(response, response_type)

def __deserialize(data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if type(klass) == str:
        if klass.startswith('list['):
            sub_kls = re.match(r'list\[(.*)\]', klass).group(1)
            return [__deserialize(sub_data, sub_kls)
                    for sub_data in data]

        if klass.startswith('dict('):
            sub_kls = re.match(r'dict\(([^,]*), (.*)\)', klass).group(2)
            return {k: __deserialize(v, sub_kls)
                    for k, v in six.iteritems(data)}

        # convert str to class
        if klass in NATIVE_TYPES_MAPPING:
            klass = NATIVE_TYPES_MAPPING[klass]
        else:
            klass = getattr(uiuc_incas_server.models, klass)

    if klass in PRIMITIVE_TYPES:
        return __deserialize_primitive(data, klass)
    elif klass == object:
        return __deserialize_object(data)
    elif klass == datetime.date:
        return __deserialize_date(data)
    elif klass == datetime.datetime:
        return __deserialize_datatime(data)
    else:
        return __deserialize_model(data, klass)

def __deserialize_file(response):
    """Deserializes body to file

    Saves response body into a file in a temporary folder,
    using the filename from the `Content-Disposition` header if provided.

    :param response:  RESTResponse.
    :return: file path.
    """
    fd, path = tempfile.mkstemp(dir=configuration.temp_folder_path)
    os.close(fd)
    os.remove(path)

    content_disposition = response.getheader("Content-Disposition")
    if content_disposition:
        filename = re.search(r'filename=[\'"]?([^\'"\s]+)[\'"]?',
                                content_disposition).group(1)
        path = os.path.join(os.path.dirname(path), filename)
        response_data = response.data
        with open(path, "wb") as f:
            if isinstance(response_data, str):
                # change str to bytes so we can write it
                response_data = response_data.encode('utf-8')
                f.write(response_data)
            else:
                f.write(response_data)
    return path

def __deserialize_primitive(data, klass):
    """Deserializes string to primitive type.

    :param data: str.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    """
    try:
        return klass(data)
    except UnicodeEncodeError:
        return six.text_type(data)
    except TypeError:
        return data

def __deserialize_object(value):
    """Return a original value.

    :return: object.
    """
    return value

def __deserialize_date(string):
    """Deserializes string to date.

    :param string: str.
    :return: date.
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string
    except ValueError:
        raise rest.ApiException(
            status=0,
            reason="Failed to parse `{0}` as date object".format(string)
        )

def __deserialize_datatime(string):
    """Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :return: datetime.
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string
    except ValueError:
        raise rest.ApiException(
            status=0,
            reason=(
                "Failed to parse `{0}` as datetime object"
                .format(string)
            )
        )

def __deserialize_model(data, klass):
    """Deserializes list or dict to model.

    :param data: dict, list.
    :param klass: class literal.
    :return: model object.
    """

    if not klass.swagger_types and not hasattr(klass, 'get_real_child_model'):
        return data

    kwargs = {}
    if klass.swagger_types is not None:
        for attr, attr_type in six.iteritems(klass.swagger_types):
            if (data is not None and
                    klass.attribute_map[attr] in data and
                    isinstance(data, (list, dict))):
                value = data[klass.attribute_map[attr]]
                kwargs[attr] = __deserialize(value, attr_type)

    instance = klass(**kwargs)

    if (isinstance(instance, dict) and
            klass.swagger_types is not None and
            isinstance(data, dict)):
        for key, value in data.items():
            if key not in klass.swagger_types:
                instance[key] = value
    if hasattr(instance, 'get_real_child_model'):
        klass_name = instance.get_real_child_model(data)
        if klass_name:
            instance = __deserialize(data, klass_name)
    return instance

def get_enrichment_pattern(prefix, enrichment_name, provider, version):
    if enrichment_name is None:
        enrichment_name = '*'
    if provider is None:
        provider = '*'
    if version is None:
        version = '*'
    return f'{prefix}:enrich:{enrichment_name}:{provider}:{version}'

def get_collection_pattern(prefix, collection_name, provider, version):
    if collection_name is None:
        collection_name = '*'
    if provider is None:
        provider = '*'
    if version is None:
        version = '*'
    return f'segment:{collection_name}:{provider}:{version}'

def get_graph_pattern(prefix, provider_name, graph_name, distance_name, version, time_stamp):
    if provider_name is None:
        provider_name = '*'
    if graph_name is None:
        graph_name = '*'
    if distance_name is None:
        distance_name = '*'
    if version is None:
        version = '*'
    if time_stamp is None:
        time_stamp = '*'
    pattern = f'{prefix}:{provider_name}:{graph_name}:{distance_name}:{version}:{time_stamp}'
    return pattern
