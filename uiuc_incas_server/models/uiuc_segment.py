# coding: utf-8

"""
    INCAS TA2-UIUC Datatypes

    This API document is defined based on INCAS Common Datatypes version 0.0.6.  # noqa: E501

    OpenAPI spec version: 1.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class UiucSegment(object):
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
        'description': 'str',
        'configurations': 'dict(str, str)',
        'members': 'dict(str, float)',
        'enrichments': 'dict(str, Enrichment)',
        'response_rate': 'dict(str, float)'
    }

    attribute_map = {
        'description': 'description',
        'configurations': 'configurations',
        'members': 'members',
        'enrichments': 'enrichments',
        'response_rate': 'responseRate'
    }

    def __init__(self, description=None, configurations=None, members=None, enrichments=None, response_rate=None):  # noqa: E501
        """UiucSegment - a model defined in Swagger"""  # noqa: E501
        self._description = None
        self._configurations = None
        self._members = None
        self._enrichments = None
        self._response_rate = None
        self.discriminator = None
        if description is not None:
            self.description = description
        if configurations is not None:
            self.configurations = configurations
        if members is not None:
            self.members = members
        if enrichments is not None:
            self.enrichments = enrichments
        if response_rate is not None:
            self.response_rate = response_rate

    @property
    def description(self):
        """Gets the description of this UiucSegment.  # noqa: E501

        Description of the segment.  # noqa: E501

        :return: The description of this UiucSegment.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UiucSegment.

        Description of the segment.  # noqa: E501

        :param description: The description of this UiucSegment.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def configurations(self):
        """Gets the configurations of this UiucSegment.  # noqa: E501

        Configuration dictionary of this segment.  # noqa: E501

        :return: The configurations of this UiucSegment.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations):
        """Sets the configurations of this UiucSegment.

        Configuration dictionary of this segment.  # noqa: E501

        :param configurations: The configurations of this UiucSegment.  # noqa: E501
        :type: dict(str, str)
        """

        self._configurations = configurations

    @property
    def members(self):
        """Gets the members of this UiucSegment.  # noqa: E501

        Membership value of actors.  # noqa: E501

        :return: The members of this UiucSegment.  # noqa: E501
        :rtype: dict(str, float)
        """
        return self._members

    @members.setter
    def members(self, members):
        """Sets the members of this UiucSegment.

        Membership value of actors.  # noqa: E501

        :param members: The members of this UiucSegment.  # noqa: E501
        :type: dict(str, float)
        """

        self._members = members

    @property
    def enrichments(self):
        """Gets the enrichments of this UiucSegment.  # noqa: E501


        :return: The enrichments of this UiucSegment.  # noqa: E501
        :rtype: dict(str, Enrichment)
        """
        return self._enrichments

    @enrichments.setter
    def enrichments(self, enrichments):
        """Sets the enrichments of this UiucSegment.


        :param enrichments: The enrichments of this UiucSegment.  # noqa: E501
        :type: dict(str, Enrichment)
        """

        self._enrichments = enrichments

    @property
    def response_rate(self):
        """Gets the response_rate of this UiucSegment.  # noqa: E501


        :return: The response_rate of this UiucSegment.  # noqa: E501
        :rtype: dict(str, float)
        """
        return self._response_rate

    @response_rate.setter
    def response_rate(self, response_rate):
        """Sets the response_rate of this UiucSegment.


        :param response_rate: The response_rate of this UiucSegment.  # noqa: E501
        :type: dict(str, float)
        """

        self._response_rate = response_rate

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
        if issubclass(UiucSegment, dict):
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
        if not isinstance(other, UiucSegment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other