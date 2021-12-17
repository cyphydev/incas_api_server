# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.base_enrichment_meta import BaseEnrichmentMeta  # noqa: F401,E501
from swagger_server import util


class TextMessageEnrichmentMeta(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, provider_name: str=None, enrichment_name: str=None, version: str=None):  # noqa: E501
        """TextMessageEnrichmentMeta - a model defined in Swagger

        :param provider_name: The provider_name of this TextMessageEnrichmentMeta.  # noqa: E501
        :type provider_name: str
        :param enrichment_name: The enrichment_name of this TextMessageEnrichmentMeta.  # noqa: E501
        :type enrichment_name: str
        :param version: The version of this TextMessageEnrichmentMeta.  # noqa: E501
        :type version: str
        """
        self.swagger_types = {
            'provider_name': str,
            'enrichment_name': str,
            'version': str
        }

        self.attribute_map = {
            'provider_name': 'providerName',
            'enrichment_name': 'enrichmentName',
            'version': 'version'
        }
        self._provider_name = provider_name
        self._enrichment_name = enrichment_name
        self._version = version

    @classmethod
    def from_dict(cls, dikt) -> 'TextMessageEnrichmentMeta':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TextMessageEnrichmentMeta of this TextMessageEnrichmentMeta.  # noqa: E501
        :rtype: TextMessageEnrichmentMeta
        """
        return util.deserialize_model(dikt, cls)

    @property
    def provider_name(self) -> str:
        """Gets the provider_name of this TextMessageEnrichmentMeta.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :return: The provider_name of this TextMessageEnrichmentMeta.
        :rtype: str
        """
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name: str):
        """Sets the provider_name of this TextMessageEnrichmentMeta.

        The team (e.g., UIUC-DMG) who provides the enrichment.  # noqa: E501

        :param provider_name: The provider_name of this TextMessageEnrichmentMeta.
        :type provider_name: str
        """

        self._provider_name = provider_name

    @property
    def enrichment_name(self) -> str:
        """Gets the enrichment_name of this TextMessageEnrichmentMeta.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :return: The enrichment_name of this TextMessageEnrichmentMeta.
        :rtype: str
        """
        return self._enrichment_name

    @enrichment_name.setter
    def enrichment_name(self, enrichment_name: str):
        """Sets the enrichment_name of this TextMessageEnrichmentMeta.

        The enrichment (e.g., Concern-Stance) name for the enrichment.  # noqa: E501

        :param enrichment_name: The enrichment_name of this TextMessageEnrichmentMeta.
        :type enrichment_name: str
        """

        self._enrichment_name = enrichment_name

    @property
    def version(self) -> str:
        """Gets the version of this TextMessageEnrichmentMeta.

        The version within the same (provider, name).  # noqa: E501

        :return: The version of this TextMessageEnrichmentMeta.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this TextMessageEnrichmentMeta.

        The version within the same (provider, name).  # noqa: E501

        :param version: The version of this TextMessageEnrichmentMeta.
        :type version: str
        """

        self._version = version
