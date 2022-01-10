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
from uiuc_incas_server.models.base_edge import BaseEdge  # noqa: F401,E501

class MessageToActorEdge(BaseEdge):
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
        'message_id': 'str',
        'actor_id': 'str',
        'action_type': 'str'
    }
    if hasattr(BaseEdge, "swagger_types"):
        swagger_types.update(BaseEdge.swagger_types)

    attribute_map = {
        'message_id': 'messageId',
        'actor_id': 'actorId',
        'action_type': 'actionType'
    }
    if hasattr(BaseEdge, "attribute_map"):
        attribute_map.update(BaseEdge.attribute_map)

    def __init__(self, message_id=None, actor_id=None, action_type=None, *args, **kwargs):  # noqa: E501
        """MessageToActorEdge - a model defined in Swagger"""  # noqa: E501
        self._message_id = None
        self._actor_id = None
        self._action_type = None
        self.discriminator = None
        if message_id is not None:
            self.message_id = message_id
        if actor_id is not None:
            self.actor_id = actor_id
        if action_type is not None:
            self.action_type = action_type
        BaseEdge.__init__(self, *args, **kwargs)

    @property
    def message_id(self):
        """Gets the message_id of this MessageToActorEdge.  # noqa: E501


        :return: The message_id of this MessageToActorEdge.  # noqa: E501
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """Sets the message_id of this MessageToActorEdge.


        :param message_id: The message_id of this MessageToActorEdge.  # noqa: E501
        :type: str
        """

        self._message_id = message_id

    @property
    def actor_id(self):
        """Gets the actor_id of this MessageToActorEdge.  # noqa: E501


        :return: The actor_id of this MessageToActorEdge.  # noqa: E501
        :rtype: str
        """
        return self._actor_id

    @actor_id.setter
    def actor_id(self, actor_id):
        """Sets the actor_id of this MessageToActorEdge.


        :param actor_id: The actor_id of this MessageToActorEdge.  # noqa: E501
        :type: str
        """

        self._actor_id = actor_id

    @property
    def action_type(self):
        """Gets the action_type of this MessageToActorEdge.  # noqa: E501


        :return: The action_type of this MessageToActorEdge.  # noqa: E501
        :rtype: str
        """
        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        """Sets the action_type of this MessageToActorEdge.


        :param action_type: The action_type of this MessageToActorEdge.  # noqa: E501
        :type: str
        """

        self._action_type = action_type

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
        if issubclass(MessageToActorEdge, dict):
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
        if not isinstance(other, MessageToActorEdge):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
