# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.base_message_enrichment import BaseMessageEnrichment  # noqa: F401,E501
from swagger_server import util


class TextMessageEnrichment(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, message_uuid: str=None, provider_name: str=None, enrichment_name: str=None, version: str=None, confidence: float=None, attribute_value: str=None):  # noqa: E501
        """TextMessageEnrichment - a model defined in Swagger

        :param message_uuid: The message_uuid of this TextMessageEnrichment.  # noqa: E501
        :type message_uuid: str
        :param provider_name: The provider_name of this TextMessageEnrichment.  # noqa: E501
        :type provider_name: str
        :param enrichment_name: The enrichment_name of this TextMessageEnrichment.  # noqa: E501
        :type enrichment_name: str
        :param version: The version of this TextMessageEnrichment.  # noqa: E501
        :type version: str
        :param confidence: The confidence of this TextMessageEnrichment.  # noqa: E501
        :type confidence: float
        :param attribute_value: The attribute_value of this TextMessageEnrichment.  # noqa: E501
        :type attribute_value: str
        """
        self.swagger_types = {
            'message_uuid': str,
            'provider_name': str,
            'enrichment_name': str,
            'version': str,
            'confidence': float,
            'attribute_value': str
        }

        self.attribute_map = {
            'message_uuid': 'messageUuid',
            'provider_name': 'providerName',
            'enrichment_name': 'enrichmentName',
            'version': 'version',
            'confidence': 'confidence',
            'attribute_value': 'attributeValue'
        }
        self._message_uuid = message_uuid
        self._provider_name = provider_name
        self._enrichment_name = enrichment_name
        self._version = version
        self._confidence = confidence
        self._attribute_value = attribute_value

    @classmethod
    def from_dict(cls, dikt) -> 'TextMessageEnrichment':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TextMessageEnrichment of this TextMessageEnrichment.  # noqa: E501
        :rtype: TextMessageEnrichment
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message_uuid(self) -> str:
        """Gets the message_uuid of this TextMessageEnrichment.


        :return: The message_uuid of this TextMessageEnrichment.
        :rtype: str
        """
        return self._message_uuid

    @message_uuid.setter
    def message_uuid(self, message_uuid: str):
        """Sets the message_uuid of this TextMessageEnrichment.


        :param message_uuid: The message_uuid of this TextMessageEnrichment.
        :type message_uuid: str
        """

        self._message_uuid = message_uuid

    @property
    def provider_name(self) -> str:
        """Gets the provider_name of this TextMessageEnrichment.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :return: The provider_name of this TextMessageEnrichment.
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name: str):
        """Sets the provider_name of this TextMessageEnrichment.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :param provider_name: The provider_name of this TextMessageEnrichment.
        :type provider_name: str
        """

        self._provider_name = provider_name

    @property
    def enrichment_name(self) -> str:
        """Gets the enrichment_name of this TextMessageEnrichment.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :return: The enrichment_name of this TextMessageEnrichment.
        :rtype: str
        """
        return self._enrichment_name

    @enrichment_name.setter
    def enrichment_name(self, enrichment_name: str):
        """Sets the enrichment_name of this TextMessageEnrichment.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :param enrichment_name: The enrichment_name of this TextMessageEnrichment.
        :type enrichment_name: str
        """

        self._enrichment_name = enrichment_name

    @property
    def version(self) -> str:
        """Gets the version of this TextMessageEnrichment.

        The version within the same (provider, name).  # noqa: E501

        :return: The version of this TextMessageEnrichment.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this TextMessageEnrichment.

        The version within the same (provider, name).  # noqa: E501

        :param version: The version of this TextMessageEnrichment.
        :type version: str
        """

        self._version = version

    @property
    def confidence(self) -> float:
        """Gets the confidence of this TextMessageEnrichment.

        The confidence that this enrichment is correct, expressed as a percentage between 0.0 and 1.0  # noqa: E501

        :return: The confidence of this TextMessageEnrichment.
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence: float):
        """Sets the confidence of this TextMessageEnrichment.

        The confidence that this enrichment is correct, expressed as a percentage between 0.0 and 1.0  # noqa: E501

        :param confidence: The confidence of this TextMessageEnrichment.
        :type confidence: float
        """

        self._confidence = confidence

    @property
    def attribute_value(self) -> str:
        """Gets the attribute_value of this TextMessageEnrichment.


        :return: The attribute_value of this TextMessageEnrichment.
        :rtype: str
        """
        return self._attribute_value

    @attribute_value.setter
    def attribute_value(self, attribute_value: str):
        """Sets the attribute_value of this TextMessageEnrichment.


        :param attribute_value: The attribute_value of this TextMessageEnrichment.
        :type attribute_value: str
        """

        self._attribute_value = attribute_value
