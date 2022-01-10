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

class BaseMessageEnrichmentMeta(object):
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
        'provider_name': 'str',
        'enrichment_name': 'str',
        'version': 'str',
        'enrichment_type': 'str'
    }

    attribute_map = {
        'provider_name': 'providerName',
        'enrichment_name': 'enrichmentName',
        'version': 'version',
        'enrichment_type': 'enrichmentType'
    }

    discriminator_value_class_map = {
            'category'.lower(): '#/components/schemas/CategoryMessageEnrichmentMeta',
            'numerical'.lower(): '#/components/schemas/NumericalMessageEnrichmentMeta',
            'array'.lower(): '#/components/schemas/ArrayMessageEnrichmentMeta',
            'text'.lower(): '#/components/schemas/TextMessageEnrichmentMeta',
    }

    def __init__(self, provider_name=None, enrichment_name=None, version=None, enrichment_type=None):  # noqa: E501
        """BaseMessageEnrichmentMeta - a model defined in Swagger"""  # noqa: E501
        self._provider_name = None
        self._enrichment_name = None
        self._version = None
        self._enrichment_type = None
        self.discriminator = 'enrichmentType'
        if provider_name is not None:
            self.provider_name = provider_name
        if enrichment_name is not None:
            self.enrichment_name = enrichment_name
        if version is not None:
            self.version = version
        self.enrichment_type = enrichment_type

    @property
    def provider_name(self):
        """Gets the provider_name of this BaseMessageEnrichmentMeta.  # noqa: E501

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :return: The provider_name of this BaseMessageEnrichmentMeta.  # noqa: E501
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name):
        """Sets the provider_name of this BaseMessageEnrichmentMeta.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :param provider_name: The provider_name of this BaseMessageEnrichmentMeta.  # noqa: E501
        :type: str
        """

        self._provider_name = provider_name

    @property
    def enrichment_name(self):
        """Gets the enrichment_name of this BaseMessageEnrichmentMeta.  # noqa: E501

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :return: The enrichment_name of this BaseMessageEnrichmentMeta.  # noqa: E501
        :rtype: str
        """
        return self._enrichment_name

    @enrichment_name.setter
    def enrichment_name(self, enrichment_name):
        """Sets the enrichment_name of this BaseMessageEnrichmentMeta.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :param enrichment_name: The enrichment_name of this BaseMessageEnrichmentMeta.  # noqa: E501
        :type: str
        """

        self._enrichment_name = enrichment_name

    @property
    def version(self):
        """Gets the version of this BaseMessageEnrichmentMeta.  # noqa: E501

        The version within the same (provider, name).  # noqa: E501

        :return: The version of this BaseMessageEnrichmentMeta.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this BaseMessageEnrichmentMeta.

        The version within the same (provider, name).  # noqa: E501

        :param version: The version of this BaseMessageEnrichmentMeta.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def enrichment_type(self):
        """Gets the enrichment_type of this BaseMessageEnrichmentMeta.  # noqa: E501

        For discriminator  # noqa: E501

        :return: The enrichment_type of this BaseMessageEnrichmentMeta.  # noqa: E501
        :rtype: str
        """
        return self._enrichment_type

    @enrichment_type.setter
    def enrichment_type(self, enrichment_type):
        """Sets the enrichment_type of this BaseMessageEnrichmentMeta.

        For discriminator  # noqa: E501

        :param enrichment_type: The enrichment_type of this BaseMessageEnrichmentMeta.  # noqa: E501
        :type: str
        """
        if enrichment_type is None:
            raise ValueError("Invalid value for `enrichment_type`, must not be `None`")  # noqa: E501
        allowed_values = ["category", "numerical", "array", "text"]  # noqa: E501
        if enrichment_type not in allowed_values:
            raise ValueError(
                "Invalid value for `enrichment_type` ({0}), must be one of {1}"  # noqa: E501
                .format(enrichment_type, allowed_values)
            )

        self._enrichment_type = enrichment_type

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
        if issubclass(BaseMessageEnrichmentMeta, dict):
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
        if not isinstance(other, BaseMessageEnrichmentMeta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
