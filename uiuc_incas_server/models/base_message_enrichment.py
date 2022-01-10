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

class BaseMessageEnrichment(object):
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
        'message_uuid': 'str',
        'provider_name': 'str',
        'enrichment_name': 'str',
        'version': 'str',
        'confidence': 'float',
        'enrichment_type': 'str'
    }

    attribute_map = {
        'message_uuid': 'messageUuid',
        'provider_name': 'providerName',
        'enrichment_name': 'enrichmentName',
        'version': 'version',
        'confidence': 'confidence',
        'enrichment_type': 'enrichmentType'
    }

    def __init__(self, message_uuid=None, provider_name=None, enrichment_name=None, version=None, confidence=None, enrichment_type=None):  # noqa: E501
        """BaseMessageEnrichment - a model defined in Swagger"""  # noqa: E501
        self._message_uuid = None
        self._provider_name = None
        self._enrichment_name = None
        self._version = None
        self._confidence = None
        self._enrichment_type = None
        self.discriminator = None
        if message_uuid is not None:
            self.message_uuid = message_uuid
        if provider_name is not None:
            self.provider_name = provider_name
        if enrichment_name is not None:
            self.enrichment_name = enrichment_name
        if version is not None:
            self.version = version
        if confidence is not None:
            self.confidence = confidence
        self.enrichment_type = enrichment_type

    @property
    def message_uuid(self):
        """Gets the message_uuid of this BaseMessageEnrichment.  # noqa: E501


        :return: The message_uuid of this BaseMessageEnrichment.  # noqa: E501
        :rtype: str
        """
        return self._message_uuid

    @message_uuid.setter
    def message_uuid(self, message_uuid):
        """Sets the message_uuid of this BaseMessageEnrichment.


        :param message_uuid: The message_uuid of this BaseMessageEnrichment.  # noqa: E501
        :type: str
        """

        self._message_uuid = message_uuid

    @property
    def provider_name(self):
        """Gets the provider_name of this BaseMessageEnrichment.  # noqa: E501

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :return: The provider_name of this BaseMessageEnrichment.  # noqa: E501
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name):
        """Sets the provider_name of this BaseMessageEnrichment.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :param provider_name: The provider_name of this BaseMessageEnrichment.  # noqa: E501
        :type: str
        """

        self._provider_name = provider_name

    @property
    def enrichment_name(self):
        """Gets the enrichment_name of this BaseMessageEnrichment.  # noqa: E501

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :return: The enrichment_name of this BaseMessageEnrichment.  # noqa: E501
        :rtype: str
        """
        return self._enrichment_name

    @enrichment_name.setter
    def enrichment_name(self, enrichment_name):
        """Sets the enrichment_name of this BaseMessageEnrichment.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :param enrichment_name: The enrichment_name of this BaseMessageEnrichment.  # noqa: E501
        :type: str
        """

        self._enrichment_name = enrichment_name

    @property
    def version(self):
        """Gets the version of this BaseMessageEnrichment.  # noqa: E501

        The version within the same (provider, name).  # noqa: E501

        :return: The version of this BaseMessageEnrichment.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this BaseMessageEnrichment.

        The version within the same (provider, name).  # noqa: E501

        :param version: The version of this BaseMessageEnrichment.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def confidence(self):
        """Gets the confidence of this BaseMessageEnrichment.  # noqa: E501

        The confidence that this enrichment is correct, expressed as a percentage between 0.0 and 1.0  # noqa: E501

        :return: The confidence of this BaseMessageEnrichment.  # noqa: E501
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """Sets the confidence of this BaseMessageEnrichment.

        The confidence that this enrichment is correct, expressed as a percentage between 0.0 and 1.0  # noqa: E501

        :param confidence: The confidence of this BaseMessageEnrichment.  # noqa: E501
        :type: float
        """

        self._confidence = confidence

    @property
    def enrichment_type(self):
        """Gets the enrichment_type of this BaseMessageEnrichment.  # noqa: E501

        For discriminator  # noqa: E501

        :return: The enrichment_type of this BaseMessageEnrichment.  # noqa: E501
        :rtype: str
        """
        return self._enrichment_type

    @enrichment_type.setter
    def enrichment_type(self, enrichment_type):
        """Sets the enrichment_type of this BaseMessageEnrichment.

        For discriminator  # noqa: E501

        :param enrichment_type: The enrichment_type of this BaseMessageEnrichment.  # noqa: E501
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
        if issubclass(BaseMessageEnrichment, dict):
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
        if not isinstance(other, BaseMessageEnrichment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
