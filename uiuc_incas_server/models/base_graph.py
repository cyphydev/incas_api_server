# coding: utf-8

"""
    INCAS TA2-UIUC Datatypes

    This API document is defined based on INCAS Common Datatypes version 0.0.3.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BaseGraph(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'graph_id': 'str',
        'provider_name': 'str',
        'graph_name': 'str',
        'distance_name': 'str',
        'version': 'str',
        'time_stamp': 'str',
        'platform': 'str',
        'graph_type': 'str'
    }

    attribute_map = {
        'graph_id': 'graphId',
        'provider_name': 'providerName',
        'graph_name': 'graphName',
        'distance_name': 'distanceName',
        'version': 'version',
        'time_stamp': 'timeStamp',
        'platform': 'platform',
        'graph_type': 'graphType'
    }

    discriminator_value_class_map = {
          'MessageMessageGraph': 'MessageMessageGraph',
'MessageMessageGraphDB': 'MessageMessageGraphDB',
'ActorActorGraphDB': 'ActorActorGraphDB',
'ActorMessageGraph': 'ActorMessageGraph',
'ActorMessageGraphDB': 'ActorMessageGraphDB',
'ActorActorGraph': 'ActorActorGraph'    }

    def __init__(self, graph_id=None, provider_name=None, graph_name=None, distance_name=None, version=None, time_stamp=None, platform=None, graph_type=None):  # noqa: E501
        """BaseGraph - a model defined in Swagger"""  # noqa: E501
        self._graph_id = None
        self._provider_name = None
        self._graph_name = None
        self._distance_name = None
        self._version = None
        self._time_stamp = None
        self._platform = None
        self._graph_type = None
        self.discriminator = 'graphType'
        if graph_id is not None:
            self.graph_id = graph_id
        if provider_name is not None:
            self.provider_name = provider_name
        if graph_name is not None:
            self.graph_name = graph_name
        if distance_name is not None:
            self.distance_name = distance_name
        if version is not None:
            self.version = version
        if time_stamp is not None:
            self.time_stamp = time_stamp
        if platform is not None:
            self.platform = platform
        self.graph_type = graph_type

    @property
    def graph_id(self):
        """Gets the graph_id of this BaseGraph.  # noqa: E501

        This is the unique ID associated to the graph instance.  # noqa: E501

        :return: The graph_id of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._graph_id

    @graph_id.setter
    def graph_id(self, graph_id):
        """Sets the graph_id of this BaseGraph.

        This is the unique ID associated to the graph instance.  # noqa: E501

        :param graph_id: The graph_id of this BaseGraph.  # noqa: E501
        :type: str
        """

        self._graph_id = graph_id

    @property
    def provider_name(self):
        """Gets the provider_name of this BaseGraph.  # noqa: E501

        The team who builds this graph.  # noqa: E501

        :return: The provider_name of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name):
        """Sets the provider_name of this BaseGraph.

        The team who builds this graph.  # noqa: E501

        :param provider_name: The provider_name of this BaseGraph.  # noqa: E501
        :type: str
        """

        self._provider_name = provider_name

    @property
    def graph_name(self):
        """Gets the graph_name of this BaseGraph.  # noqa: E501

        The name assigned to the algorithm/method used to construct the graph.  # noqa: E501

        :return: The graph_name of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._graph_name

    @graph_name.setter
    def graph_name(self, graph_name):
        """Sets the graph_name of this BaseGraph.

        The name assigned to the algorithm/method used to construct the graph.  # noqa: E501

        :param graph_name: The graph_name of this BaseGraph.  # noqa: E501
        :type: str
        """

        self._graph_name = graph_name

    @property
    def distance_name(self):
        """Gets the distance_name of this BaseGraph.  # noqa: E501

        The distance function used to build the graph.  # noqa: E501

        :return: The distance_name of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._distance_name

    @distance_name.setter
    def distance_name(self, distance_name):
        """Sets the distance_name of this BaseGraph.

        The distance function used to build the graph.  # noqa: E501

        :param distance_name: The distance_name of this BaseGraph.  # noqa: E501
        :type: str
        """

        self._distance_name = distance_name

    @property
    def version(self):
        """Gets the version of this BaseGraph.  # noqa: E501

        The version ID within the same (providerName, graphName, distanceName)  # noqa: E501

        :return: The version of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this BaseGraph.

        The version ID within the same (providerName, graphName, distanceName)  # noqa: E501

        :param version: The version of this BaseGraph.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def time_stamp(self):
        """Gets the time_stamp of this BaseGraph.  # noqa: E501

        Used for distinguishing the dynamic graph on time dimension.  # noqa: E501

        :return: The time_stamp of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, time_stamp):
        """Sets the time_stamp of this BaseGraph.

        Used for distinguishing the dynamic graph on time dimension.  # noqa: E501

        :param time_stamp: The time_stamp of this BaseGraph.  # noqa: E501
        :type: str
        """

        self._time_stamp = time_stamp

    @property
    def platform(self):
        """Gets the platform of this BaseGraph.  # noqa: E501


        :return: The platform of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this BaseGraph.


        :param platform: The platform of this BaseGraph.  # noqa: E501
        :type: str
        """
        allowed_values = ["MEDIA_UNSPECIFIED", "News", "Reddit", "Twitter", "Webpage"]  # noqa: E501
        if platform not in allowed_values:
            raise ValueError(
                "Invalid value for `platform` ({0}), must be one of {1}"  # noqa: E501
                .format(platform, allowed_values)
            )

        self._platform = platform

    @property
    def graph_type(self):
        """Gets the graph_type of this BaseGraph.  # noqa: E501

        For discriminator  # noqa: E501

        :return: The graph_type of this BaseGraph.  # noqa: E501
        :rtype: str
        """
        return self._graph_type

    @graph_type.setter
    def graph_type(self, graph_type):
        """Sets the graph_type of this BaseGraph.

        For discriminator  # noqa: E501

        :param graph_type: The graph_type of this BaseGraph.  # noqa: E501
        :type: str
        """
        if graph_type is None:
            raise ValueError("Invalid value for `graph_type`, must not be `None`")  # noqa: E501
        allowed_values = ["MessageMessageGraph", "ActorActorGraph", "ActorMessageGraph"]  # noqa: E501
        if graph_type not in allowed_values:
            raise ValueError(
                "Invalid value for `graph_type` ({0}), must be one of {1}"  # noqa: E501
                .format(graph_type, allowed_values)
            )

        self._graph_type = graph_type

    def get_real_child_model(self, data):
        """Returns the real base class specified by the discriminator"""
        discriminator_value = data[self.discriminator].lower()
        return self.discriminator_value_class_map.get(discriminator_value)

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(BaseGraph, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BaseGraph):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
