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
from uiuc_incas_server.models.base_message_enrichment import BaseMessageEnrichment  # noqa: F401,E501

class TextMessageEnrichment(BaseMessageEnrichment):
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
        'attribute_value': 'str'
    }
    if hasattr(BaseMessageEnrichment, "swagger_types"):
        swagger_types.update(BaseMessageEnrichment.swagger_types)

    attribute_map = {
        'attribute_value': 'attributeValue'
    }
    if hasattr(BaseMessageEnrichment, "attribute_map"):
        attribute_map.update(BaseMessageEnrichment.attribute_map)

    def __init__(self, attribute_value=None, *args, **kwargs):  # noqa: E501
        """TextMessageEnrichment - a model defined in Swagger"""  # noqa: E501
        self._attribute_value = None
        self.discriminator = None
        if attribute_value is not None:
            self.attribute_value = attribute_value
        BaseMessageEnrichment.__init__(self, *args, **kwargs)

    @property
    def attribute_value(self):
        """Gets the attribute_value of this TextMessageEnrichment.  # noqa: E501


        :return: The attribute_value of this TextMessageEnrichment.  # noqa: E501
        :rtype: str
        """
        return self._attribute_value

    @attribute_value.setter
    def attribute_value(self, attribute_value):
        """Sets the attribute_value of this TextMessageEnrichment.


        :param attribute_value: The attribute_value of this TextMessageEnrichment.  # noqa: E501
        :type: str
        """

        self._attribute_value = attribute_value

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
        if issubclass(TextMessageEnrichment, dict):
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
        if not isinstance(other, TextMessageEnrichment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
