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

class ActorSegmentsBatchDeleteBody(object):
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
        'ids': 'list[str]',
        'collection_name': 'str',
        'provider_name': 'str',
        'version': 'str'
    }

    attribute_map = {
        'ids': 'ids',
        'collection_name': 'collectionName',
        'provider_name': 'providerName',
        'version': 'version'
    }

    def __init__(self, ids=None, collection_name=None, provider_name=None, version=None):  # noqa: E501
        """ActorSegmentsBatchDeleteBody - a model defined in Swagger"""  # noqa: E501
        self._ids = None
        self._collection_name = None
        self._provider_name = None
        self._version = None
        self.discriminator = None
        self.ids = ids
        self.collection_name = collection_name
        self.provider_name = provider_name
        self.version = version

    @property
    def ids(self):
        """Gets the ids of this ActorSegmentsBatchDeleteBody.  # noqa: E501


        :return: The ids of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :rtype: list[str]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """Sets the ids of this ActorSegmentsBatchDeleteBody.


        :param ids: The ids of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :type: list[str]
        """
        if ids is None:
            raise ValueError("Invalid value for `ids`, must not be `None`")  # noqa: E501

        self._ids = ids

    @property
    def collection_name(self):
        """Gets the collection_name of this ActorSegmentsBatchDeleteBody.  # noqa: E501


        :return: The collection_name of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :rtype: str
        """
        return self._collection_name

    @collection_name.setter
    def collection_name(self, collection_name):
        """Sets the collection_name of this ActorSegmentsBatchDeleteBody.


        :param collection_name: The collection_name of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :type: str
        """
        if collection_name is None:
            raise ValueError("Invalid value for `collection_name`, must not be `None`")  # noqa: E501

        self._collection_name = collection_name

    @property
    def provider_name(self):
        """Gets the provider_name of this ActorSegmentsBatchDeleteBody.  # noqa: E501


        :return: The provider_name of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name):
        """Sets the provider_name of this ActorSegmentsBatchDeleteBody.


        :param provider_name: The provider_name of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :type: str
        """
        if provider_name is None:
            raise ValueError("Invalid value for `provider_name`, must not be `None`")  # noqa: E501

        self._provider_name = provider_name

    @property
    def version(self):
        """Gets the version of this ActorSegmentsBatchDeleteBody.  # noqa: E501


        :return: The version of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ActorSegmentsBatchDeleteBody.


        :param version: The version of this ActorSegmentsBatchDeleteBody.  # noqa: E501
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

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
        if issubclass(ActorSegmentsBatchDeleteBody, dict):
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
        if not isinstance(other, ActorSegmentsBatchDeleteBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other