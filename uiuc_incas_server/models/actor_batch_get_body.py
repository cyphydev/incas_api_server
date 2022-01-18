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

class ActorBatchGetBody(object):
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
        'with_enrichment': 'bool',
        'with_segment': 'bool',
        'enrichment_name': 'str',
        'enrichment_provider_name': 'str',
        'enrichment_version': 'str',
        'collection_name': 'str',
        'collection_provider_name': 'str',
        'collection_version': 'str',
        'dev': 'bool'
    }

    attribute_map = {
        'ids': 'ids',
        'with_enrichment': 'withEnrichment',
        'with_segment': 'withSegment',
        'enrichment_name': 'enrichmentName',
        'enrichment_provider_name': 'enrichmentProviderName',
        'enrichment_version': 'enrichmentVersion',
        'collection_name': 'collectionName',
        'collection_provider_name': 'collectionProviderName',
        'collection_version': 'collectionVersion',
        'dev': 'dev'
    }

    def __init__(self, ids=None, with_enrichment=None, with_segment=None, enrichment_name=None, enrichment_provider_name=None, enrichment_version=None, collection_name=None, collection_provider_name=None, collection_version=None, dev=None):  # noqa: E501
        """ActorBatchGetBody - a model defined in Swagger"""  # noqa: E501
        self._ids = None
        self._with_enrichment = None
        self._with_segment = None
        self._enrichment_name = None
        self._enrichment_provider_name = None
        self._enrichment_version = None
        self._collection_name = None
        self._collection_provider_name = None
        self._collection_version = None
        self._dev = None
        self.discriminator = None
        self.ids = ids
        if with_enrichment is not None:
            self.with_enrichment = with_enrichment
        if with_segment is not None:
            self.with_segment = with_segment
        if enrichment_name is not None:
            self.enrichment_name = enrichment_name
        if enrichment_provider_name is not None:
            self.enrichment_provider_name = enrichment_provider_name
        if enrichment_version is not None:
            self.enrichment_version = enrichment_version
        if collection_name is not None:
            self.collection_name = collection_name
        if collection_provider_name is not None:
            self.collection_provider_name = collection_provider_name
        if collection_version is not None:
            self.collection_version = collection_version
        if dev is not None:
            self.dev = dev

    @property
    def ids(self):
        """Gets the ids of this ActorBatchGetBody.  # noqa: E501


        :return: The ids of this ActorBatchGetBody.  # noqa: E501
        :rtype: list[str]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """Sets the ids of this ActorBatchGetBody.


        :param ids: The ids of this ActorBatchGetBody.  # noqa: E501
        :type: list[str]
        """
        if ids is None:
            raise ValueError("Invalid value for `ids`, must not be `None`")  # noqa: E501

        self._ids = ids

    @property
    def with_enrichment(self):
        """Gets the with_enrichment of this ActorBatchGetBody.  # noqa: E501


        :return: The with_enrichment of this ActorBatchGetBody.  # noqa: E501
        :rtype: bool
        """
        return self._with_enrichment

    @with_enrichment.setter
    def with_enrichment(self, with_enrichment):
        """Sets the with_enrichment of this ActorBatchGetBody.


        :param with_enrichment: The with_enrichment of this ActorBatchGetBody.  # noqa: E501
        :type: bool
        """

        self._with_enrichment = with_enrichment

    @property
    def with_segment(self):
        """Gets the with_segment of this ActorBatchGetBody.  # noqa: E501


        :return: The with_segment of this ActorBatchGetBody.  # noqa: E501
        :rtype: bool
        """
        return self._with_segment

    @with_segment.setter
    def with_segment(self, with_segment):
        """Sets the with_segment of this ActorBatchGetBody.


        :param with_segment: The with_segment of this ActorBatchGetBody.  # noqa: E501
        :type: bool
        """

        self._with_segment = with_segment

    @property
    def enrichment_name(self):
        """Gets the enrichment_name of this ActorBatchGetBody.  # noqa: E501


        :return: The enrichment_name of this ActorBatchGetBody.  # noqa: E501
        :rtype: str
        """
        return self._enrichment_name

    @enrichment_name.setter
    def enrichment_name(self, enrichment_name):
        """Sets the enrichment_name of this ActorBatchGetBody.


        :param enrichment_name: The enrichment_name of this ActorBatchGetBody.  # noqa: E501
        :type: str
        """

        self._enrichment_name = enrichment_name

    @property
    def enrichment_provider_name(self):
        """Gets the enrichment_provider_name of this ActorBatchGetBody.  # noqa: E501


        :return: The enrichment_provider_name of this ActorBatchGetBody.  # noqa: E501
        :rtype: str
        """
        return self._enrichment_provider_name

    @enrichment_provider_name.setter
    def enrichment_provider_name(self, enrichment_provider_name):
        """Sets the enrichment_provider_name of this ActorBatchGetBody.


        :param enrichment_provider_name: The enrichment_provider_name of this ActorBatchGetBody.  # noqa: E501
        :type: str
        """

        self._enrichment_provider_name = enrichment_provider_name

    @property
    def enrichment_version(self):
        """Gets the enrichment_version of this ActorBatchGetBody.  # noqa: E501


        :return: The enrichment_version of this ActorBatchGetBody.  # noqa: E501
        :rtype: str
        """
        return self._enrichment_version

    @enrichment_version.setter
    def enrichment_version(self, enrichment_version):
        """Sets the enrichment_version of this ActorBatchGetBody.


        :param enrichment_version: The enrichment_version of this ActorBatchGetBody.  # noqa: E501
        :type: str
        """

        self._enrichment_version = enrichment_version

    @property
    def collection_name(self):
        """Gets the collection_name of this ActorBatchGetBody.  # noqa: E501


        :return: The collection_name of this ActorBatchGetBody.  # noqa: E501
        :rtype: str
        """
        return self._collection_name

    @collection_name.setter
    def collection_name(self, collection_name):
        """Sets the collection_name of this ActorBatchGetBody.


        :param collection_name: The collection_name of this ActorBatchGetBody.  # noqa: E501
        :type: str
        """

        self._collection_name = collection_name

    @property
    def collection_provider_name(self):
        """Gets the collection_provider_name of this ActorBatchGetBody.  # noqa: E501


        :return: The collection_provider_name of this ActorBatchGetBody.  # noqa: E501
        :rtype: str
        """
        return self._collection_provider_name

    @collection_provider_name.setter
    def collection_provider_name(self, collection_provider_name):
        """Sets the collection_provider_name of this ActorBatchGetBody.


        :param collection_provider_name: The collection_provider_name of this ActorBatchGetBody.  # noqa: E501
        :type: str
        """

        self._collection_provider_name = collection_provider_name

    @property
    def collection_version(self):
        """Gets the collection_version of this ActorBatchGetBody.  # noqa: E501


        :return: The collection_version of this ActorBatchGetBody.  # noqa: E501
        :rtype: str
        """
        return self._collection_version

    @collection_version.setter
    def collection_version(self, collection_version):
        """Sets the collection_version of this ActorBatchGetBody.


        :param collection_version: The collection_version of this ActorBatchGetBody.  # noqa: E501
        :type: str
        """

        self._collection_version = collection_version

    @property
    def dev(self):
        """Gets the dev of this ActorBatchGetBody.  # noqa: E501


        :return: The dev of this ActorBatchGetBody.  # noqa: E501
        :rtype: bool
        """
        return self._dev

    @dev.setter
    def dev(self, dev):
        """Sets the dev of this ActorBatchGetBody.


        :param dev: The dev of this ActorBatchGetBody.  # noqa: E501
        :type: bool
        """

        self._dev = dev

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
        if issubclass(ActorBatchGetBody, dict):
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
        if not isinstance(other, ActorBatchGetBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
