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

class MessageToMessageEdge(BaseEdge):
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
        'src_message_id': 'str',
        'dst_message_id': 'str',
        'weight': 'float'
    }
    if hasattr(BaseEdge, "swagger_types"):
        swagger_types.update(BaseEdge.swagger_types)

    attribute_map = {
        'src_message_id': 'srcMessageId',
        'dst_message_id': 'dstMessageId',
        'weight': 'weight'
    }
    if hasattr(BaseEdge, "attribute_map"):
        attribute_map.update(BaseEdge.attribute_map)

    def __init__(self, src_message_id=None, dst_message_id=None, weight=None, *args, **kwargs):  # noqa: E501
        """MessageToMessageEdge - a model defined in Swagger"""  # noqa: E501
        self._src_message_id = None
        self._dst_message_id = None
        self._weight = None
        self.discriminator = None
        if src_message_id is not None:
            self.src_message_id = src_message_id
        if dst_message_id is not None:
            self.dst_message_id = dst_message_id
        if weight is not None:
            self.weight = weight
        BaseEdge.__init__(self, *args, **kwargs)

    @property
    def src_message_id(self):
        """Gets the src_message_id of this MessageToMessageEdge.  # noqa: E501


        :return: The src_message_id of this MessageToMessageEdge.  # noqa: E501
        :rtype: str
        """
        return self._src_message_id

    @src_message_id.setter
    def src_message_id(self, src_message_id):
        """Sets the src_message_id of this MessageToMessageEdge.


        :param src_message_id: The src_message_id of this MessageToMessageEdge.  # noqa: E501
        :type: str
        """

        self._src_message_id = src_message_id

    @property
    def dst_message_id(self):
        """Gets the dst_message_id of this MessageToMessageEdge.  # noqa: E501


        :return: The dst_message_id of this MessageToMessageEdge.  # noqa: E501
        :rtype: str
        """
        return self._dst_message_id

    @dst_message_id.setter
    def dst_message_id(self, dst_message_id):
        """Sets the dst_message_id of this MessageToMessageEdge.


        :param dst_message_id: The dst_message_id of this MessageToMessageEdge.  # noqa: E501
        :type: str
        """

        self._dst_message_id = dst_message_id

    @property
    def weight(self):
        """Gets the weight of this MessageToMessageEdge.  # noqa: E501


        :return: The weight of this MessageToMessageEdge.  # noqa: E501
        :rtype: float
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this MessageToMessageEdge.


        :param weight: The weight of this MessageToMessageEdge.  # noqa: E501
        :type: float
        """

        self._weight = weight

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
        if issubclass(MessageToMessageEdge, dict):
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
        if not isinstance(other, MessageToMessageEdge):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
