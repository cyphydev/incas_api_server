# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class BaseMessageEnrichment(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, message_uuid: str=None, provider_name: str=None, enrichment_name: str=None, version: str=None, confidence: float=None):  # noqa: E501
        """BaseMessageEnrichment - a model defined in Swagger

        :param message_uuid: The message_uuid of this BaseMessageEnrichment.  # noqa: E501
        :type message_uuid: str
        :param provider_name: The provider_name of this BaseMessageEnrichment.  # noqa: E501
        :type provider_name: str
        :param enrichment_name: The enrichment_name of this BaseMessageEnrichment.  # noqa: E501
        :type enrichment_name: str
        :param version: The version of this BaseMessageEnrichment.  # noqa: E501
        :type version: str
        :param confidence: The confidence of this BaseMessageEnrichment.  # noqa: E501
        :type confidence: float
        """
        self.swagger_types = {
            'message_uuid': str,
            'provider_name': str,
            'enrichment_name': str,
            'version': str,
            'confidence': float
        }

        self.attribute_map = {
            'message_uuid': 'messageUuid',
            'provider_name': 'providerName',
            'enrichment_name': 'enrichmentName',
            'version': 'version',
            'confidence': 'confidence'
        }
        self._message_uuid = message_uuid
        self._provider_name = provider_name
        self._enrichment_name = enrichment_name
        self._version = version
        self._confidence = confidence

    @classmethod
    def from_dict(cls, dikt) -> 'BaseMessageEnrichment':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The BaseMessageEnrichment of this BaseMessageEnrichment.  # noqa: E501
        :rtype: BaseMessageEnrichment
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message_uuid(self) -> str:
        """Gets the message_uuid of this BaseMessageEnrichment.


        :return: The message_uuid of this BaseMessageEnrichment.
        :rtype: str
        """
        return self._message_uuid

    @message_uuid.setter
    def message_uuid(self, message_uuid: str):
        """Sets the message_uuid of this BaseMessageEnrichment.


        :param message_uuid: The message_uuid of this BaseMessageEnrichment.
        :type message_uuid: str
        """

        self._message_uuid = message_uuid

    @property
    def provider_name(self) -> str:
        """Gets the provider_name of this BaseMessageEnrichment.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :return: The provider_name of this BaseMessageEnrichment.
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name: str):
        """Sets the provider_name of this BaseMessageEnrichment.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :param provider_name: The provider_name of this BaseMessageEnrichment.
        :type provider_name: str
        """

        self._provider_name = provider_name

    @property
    def enrichment_name(self) -> str:
        """Gets the enrichment_name of this BaseMessageEnrichment.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :return: The enrichment_name of this BaseMessageEnrichment.
        :rtype: str
        """
        return self._enrichment_name

    @enrichment_name.setter
    def enrichment_name(self, enrichment_name: str):
        """Sets the enrichment_name of this BaseMessageEnrichment.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :param enrichment_name: The enrichment_name of this BaseMessageEnrichment.
        :type enrichment_name: str
        """

        self._enrichment_name = enrichment_name

    @property
    def version(self) -> str:
        """Gets the version of this BaseMessageEnrichment.

        The version within the same (provider, name).  # noqa: E501

        :return: The version of this BaseMessageEnrichment.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this BaseMessageEnrichment.

        The version within the same (provider, name).  # noqa: E501

        :param version: The version of this BaseMessageEnrichment.
        :type version: str
        """

        self._version = version

    @property
    def confidence(self) -> float:
        """Gets the confidence of this BaseMessageEnrichment.

        The confidence that this enrichment is correct, expressed as a percentage between 0.0 and 1.0  # noqa: E501

        :return: The confidence of this BaseMessageEnrichment.
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence: float):
        """Sets the confidence of this BaseMessageEnrichment.

        The confidence that this enrichment is correct, expressed as a percentage between 0.0 and 1.0  # noqa: E501

        :param confidence: The confidence of this BaseMessageEnrichment.
        :type confidence: float
        """

        self._confidence = confidence
