# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.annotation import Annotation  # noqa: F401,E501
from swagger_server.models.extra_attribute import ExtraAttribute  # noqa: F401,E501
from swagger_server.models.links import Links  # noqa: F401,E501
from swagger_server.models.media_resource import MediaResource  # noqa: F401,E501
from swagger_server import util


class Actor(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, id: str=None, actor_name: str=None, links: Links=None, entity_type: str=None, media_resources: List[MediaResource]=None, knowledge_base_url: str=None, language: str=None, description: str=None, annotations: List[Annotation]=None, extra_attributes: List[ExtraAttribute]=None):  # noqa: E501
        """Actor - a model defined in Swagger

        :param name: The name of this Actor.  # noqa: E501
        :type name: str
        :param id: The id of this Actor.  # noqa: E501
        :type id: str
        :param actor_name: The actor_name of this Actor.  # noqa: E501
        :type actor_name: str
        :param links: The links of this Actor.  # noqa: E501
        :type links: Links
        :param entity_type: The entity_type of this Actor.  # noqa: E501
        :type entity_type: str
        :param media_resources: The media_resources of this Actor.  # noqa: E501
        :type media_resources: List[MediaResource]
        :param knowledge_base_url: The knowledge_base_url of this Actor.  # noqa: E501
        :type knowledge_base_url: str
        :param language: The language of this Actor.  # noqa: E501
        :type language: str
        :param description: The description of this Actor.  # noqa: E501
        :type description: str
        :param annotations: The annotations of this Actor.  # noqa: E501
        :type annotations: List[Annotation]
        :param extra_attributes: The extra_attributes of this Actor.  # noqa: E501
        :type extra_attributes: List[ExtraAttribute]
        """
        self.swagger_types = {
            'name': str,
            'id': str,
            'actor_name': str,
            'links': Links,
            'entity_type': str,
            'media_resources': List[MediaResource],
            'knowledge_base_url': str,
            'language': str,
            'description': str,
            'annotations': List[Annotation],
            'extra_attributes': List[ExtraAttribute]
        }

        self.attribute_map = {
            'name': 'name',
            'id': 'id',
            'actor_name': 'actorName',
            'links': 'links',
            'entity_type': 'entityType',
            'media_resources': 'mediaResources',
            'knowledge_base_url': 'knowledgeBaseUrl',
            'language': 'language',
            'description': 'description',
            'annotations': 'annotations',
            'extra_attributes': 'extraAttributes'
        }
        self._name = name
        self._id = id
        self._actor_name = actor_name
        self._links = links
        self._entity_type = entity_type
        self._media_resources = media_resources
        self._knowledge_base_url = knowledge_base_url
        self._language = language
        self._description = description
        self._annotations = annotations
        self._extra_attributes = extra_attributes

    @classmethod
    def from_dict(cls, dikt) -> 'Actor':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Actor of this Actor.  # noqa: E501
        :rtype: Actor
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Actor.


        :return: The name of this Actor.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Actor.


        :param name: The name of this Actor.
        :type name: str
        """

        self._name = name

    @property
    def id(self) -> str:
        """Gets the id of this Actor.


        :return: The id of this Actor.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Actor.


        :param id: The id of this Actor.
        :type id: str
        """

        self._id = id

    @property
    def actor_name(self) -> str:
        """Gets the actor_name of this Actor.


        :return: The actor_name of this Actor.
        :rtype: str
        """
        return self._actor_name

    @actor_name.setter
    def actor_name(self, actor_name: str):
        """Sets the actor_name of this Actor.


        :param actor_name: The actor_name of this Actor.
        :type actor_name: str
        """

        self._actor_name = actor_name

    @property
    def links(self) -> Links:
        """Gets the links of this Actor.


        :return: The links of this Actor.
        :rtype: Links
        """
        return self._links

    @links.setter
    def links(self, links: Links):
        """Sets the links of this Actor.


        :param links: The links of this Actor.
        :type links: Links
        """

        self._links = links

    @property
    def entity_type(self) -> str:
        """Gets the entity_type of this Actor.


        :return: The entity_type of this Actor.
        :rtype: str
        """
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type: str):
        """Sets the entity_type of this Actor.


        :param entity_type: The entity_type of this Actor.
        :type entity_type: str
        """
        allowed_values = ["ENTITY_UNSPECIFIED", "Person", "Media", "Organization", "Government"]  # noqa: E501
        if entity_type not in allowed_values:
            raise ValueError(
                "Invalid value for `entity_type` ({0}), must be one of {1}"
                .format(entity_type, allowed_values)
            )

        self._entity_type = entity_type

    @property
    def media_resources(self) -> List[MediaResource]:
        """Gets the media_resources of this Actor.


        :return: The media_resources of this Actor.
        :rtype: List[MediaResource]
        """
        return self._media_resources

    @media_resources.setter
    def media_resources(self, media_resources: List[MediaResource]):
        """Sets the media_resources of this Actor.


        :param media_resources: The media_resources of this Actor.
        :type media_resources: List[MediaResource]
        """

        self._media_resources = media_resources

    @property
    def knowledge_base_url(self) -> str:
        """Gets the knowledge_base_url of this Actor.


        :return: The knowledge_base_url of this Actor.
        :rtype: str
        """
        return self._knowledge_base_url

    @knowledge_base_url.setter
    def knowledge_base_url(self, knowledge_base_url: str):
        """Sets the knowledge_base_url of this Actor.


        :param knowledge_base_url: The knowledge_base_url of this Actor.
        :type knowledge_base_url: str
        """

        self._knowledge_base_url = knowledge_base_url

    @property
    def language(self) -> str:
        """Gets the language of this Actor.


        :return: The language of this Actor.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language: str):
        """Sets the language of this Actor.


        :param language: The language of this Actor.
        :type language: str
        """

        self._language = language

    @property
    def description(self) -> str:
        """Gets the description of this Actor.


        :return: The description of this Actor.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Actor.


        :param description: The description of this Actor.
        :type description: str
        """

        self._description = description

    @property
    def annotations(self) -> List[Annotation]:
        """Gets the annotations of this Actor.


        :return: The annotations of this Actor.
        :rtype: List[Annotation]
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations: List[Annotation]):
        """Sets the annotations of this Actor.


        :param annotations: The annotations of this Actor.
        :type annotations: List[Annotation]
        """

        self._annotations = annotations

    @property
    def extra_attributes(self) -> List[ExtraAttribute]:
        """Gets the extra_attributes of this Actor.


        :return: The extra_attributes of this Actor.
        :rtype: List[ExtraAttribute]
        """
        return self._extra_attributes

    @extra_attributes.setter
    def extra_attributes(self, extra_attributes: List[ExtraAttribute]):
        """Sets the extra_attributes of this Actor.


        :param extra_attributes: The extra_attributes of this Actor.
        :type extra_attributes: List[ExtraAttribute]
        """

        self._extra_attributes = extra_attributes
