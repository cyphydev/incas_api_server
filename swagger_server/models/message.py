# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.actor import Actor  # noqa: F401,E501
from swagger_server.models.annotation import Annotation  # noqa: F401,E501
from swagger_server.models.extra_attribute import ExtraAttribute  # noqa: F401,E501
from swagger_server.models.geo_location import GeoLocation  # noqa: F401,E501
from swagger_server.models.one_of_media_type_attributes import OneOfMediaTypeAttributes  # noqa: F401,E501
from swagger_server import util


class Message(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, id: str=None, title: str=None, content_text: str=None, author_actor: Actor=None, media_type: str=None, media_type_attributes: OneOfMediaTypeAttributes=None, time_published: int=None, geolocation: GeoLocation=None, language: str=None, embedded_urls: List[str]=None, image_urls: List[str]=None, data_tags: List[str]=None, annotations: List[Annotation]=None, extra_attributes: List[ExtraAttribute]=None):  # noqa: E501
        """Message - a model defined in Swagger

        :param name: The name of this Message.  # noqa: E501
        :type name: str
        :param id: The id of this Message.  # noqa: E501
        :type id: str
        :param title: The title of this Message.  # noqa: E501
        :type title: str
        :param content_text: The content_text of this Message.  # noqa: E501
        :type content_text: str
        :param author_actor: The author_actor of this Message.  # noqa: E501
        :type author_actor: Actor
        :param media_type: The media_type of this Message.  # noqa: E501
        :type media_type: str
        :param media_type_attributes: The media_type_attributes of this Message.  # noqa: E501
        :type media_type_attributes: OneOfMediaTypeAttributes
        :param time_published: The time_published of this Message.  # noqa: E501
        :type time_published: int
        :param geolocation: The geolocation of this Message.  # noqa: E501
        :type geolocation: GeoLocation
        :param language: The language of this Message.  # noqa: E501
        :type language: str
        :param embedded_urls: The embedded_urls of this Message.  # noqa: E501
        :type embedded_urls: List[str]
        :param image_urls: The image_urls of this Message.  # noqa: E501
        :type image_urls: List[str]
        :param data_tags: The data_tags of this Message.  # noqa: E501
        :type data_tags: List[str]
        :param annotations: The annotations of this Message.  # noqa: E501
        :type annotations: List[Annotation]
        :param extra_attributes: The extra_attributes of this Message.  # noqa: E501
        :type extra_attributes: List[ExtraAttribute]
        """
        self.swagger_types = {
            'name': str,
            'id': str,
            'title': str,
            'content_text': str,
            'author_actor': Actor,
            'media_type': str,
            'media_type_attributes': OneOfMediaTypeAttributes,
            'time_published': int,
            'geolocation': GeoLocation,
            'language': str,
            'embedded_urls': List[str],
            'image_urls': List[str],
            'data_tags': List[str],
            'annotations': List[Annotation],
            'extra_attributes': List[ExtraAttribute]
        }

        self.attribute_map = {
            'name': 'name',
            'id': 'id',
            'title': 'title',
            'content_text': 'contentText',
            'author_actor': 'authorActor',
            'media_type': 'mediaType',
            'media_type_attributes': 'mediaTypeAttributes',
            'time_published': 'timePublished',
            'geolocation': 'geolocation',
            'language': 'language',
            'embedded_urls': 'embeddedUrls',
            'image_urls': 'imageUrls',
            'data_tags': 'dataTags',
            'annotations': 'annotations',
            'extra_attributes': 'extraAttributes'
        }
        self._name = name
        self._id = id
        self._title = title
        self._content_text = content_text
        self._author_actor = author_actor
        self._media_type = media_type
        self._media_type_attributes = media_type_attributes
        self._time_published = time_published
        self._geolocation = geolocation
        self._language = language
        self._embedded_urls = embedded_urls
        self._image_urls = image_urls
        self._data_tags = data_tags
        self._annotations = annotations
        self._extra_attributes = extra_attributes

    @classmethod
    def from_dict(cls, dikt) -> 'Message':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Message of this Message.  # noqa: E501
        :rtype: Message
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Message.


        :return: The name of this Message.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Message.


        :param name: The name of this Message.
        :type name: str
        """

        self._name = name

    @property
    def id(self) -> str:
        """Gets the id of this Message.


        :return: The id of this Message.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Message.


        :param id: The id of this Message.
        :type id: str
        """

        self._id = id

    @property
    def title(self) -> str:
        """Gets the title of this Message.


        :return: The title of this Message.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Message.


        :param title: The title of this Message.
        :type title: str
        """

        self._title = title

    @property
    def content_text(self) -> str:
        """Gets the content_text of this Message.


        :return: The content_text of this Message.
        :rtype: str
        """
        return self._content_text

    @content_text.setter
    def content_text(self, content_text: str):
        """Sets the content_text of this Message.


        :param content_text: The content_text of this Message.
        :type content_text: str
        """

        self._content_text = content_text

    @property
    def author_actor(self) -> Actor:
        """Gets the author_actor of this Message.


        :return: The author_actor of this Message.
        :rtype: Actor
        """
        return self._author_actor

    @author_actor.setter
    def author_actor(self, author_actor: Actor):
        """Sets the author_actor of this Message.


        :param author_actor: The author_actor of this Message.
        :type author_actor: Actor
        """

        self._author_actor = author_actor

    @property
    def media_type(self) -> str:
        """Gets the media_type of this Message.


        :return: The media_type of this Message.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type: str):
        """Sets the media_type of this Message.


        :param media_type: The media_type of this Message.
        :type media_type: str
        """
        allowed_values = ["MEDIA_UNSPECIFIED", "News", "Reddit", "Twitter", "Webpage"]  # noqa: E501
        if media_type not in allowed_values:
            raise ValueError(
                "Invalid value for `media_type` ({0}), must be one of {1}"
                .format(media_type, allowed_values)
            )

        self._media_type = media_type

    @property
    def media_type_attributes(self) -> OneOfMediaTypeAttributes:
        """Gets the media_type_attributes of this Message.


        :return: The media_type_attributes of this Message.
        :rtype: OneOfMediaTypeAttributes
        """
        return self._media_type_attributes

    @media_type_attributes.setter
    def media_type_attributes(self, media_type_attributes: OneOfMediaTypeAttributes):
        """Sets the media_type_attributes of this Message.


        :param media_type_attributes: The media_type_attributes of this Message.
        :type media_type_attributes: OneOfMediaTypeAttributes
        """

        self._media_type_attributes = media_type_attributes

    @property
    def time_published(self) -> int:
        """Gets the time_published of this Message.


        :return: The time_published of this Message.
        :rtype: int
        """
        return self._time_published

    @time_published.setter
    def time_published(self, time_published: int):
        """Sets the time_published of this Message.


        :param time_published: The time_published of this Message.
        :type time_published: int
        """

        self._time_published = time_published

    @property
    def geolocation(self) -> GeoLocation:
        """Gets the geolocation of this Message.


        :return: The geolocation of this Message.
        :rtype: GeoLocation
        """
        return self._geolocation

    @geolocation.setter
    def geolocation(self, geolocation: GeoLocation):
        """Sets the geolocation of this Message.


        :param geolocation: The geolocation of this Message.
        :type geolocation: GeoLocation
        """

        self._geolocation = geolocation

    @property
    def language(self) -> str:
        """Gets the language of this Message.


        :return: The language of this Message.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language: str):
        """Sets the language of this Message.


        :param language: The language of this Message.
        :type language: str
        """

        self._language = language

    @property
    def embedded_urls(self) -> List[str]:
        """Gets the embedded_urls of this Message.


        :return: The embedded_urls of this Message.
        :rtype: List[str]
        """
        return self._embedded_urls

    @embedded_urls.setter
    def embedded_urls(self, embedded_urls: List[str]):
        """Sets the embedded_urls of this Message.


        :param embedded_urls: The embedded_urls of this Message.
        :type embedded_urls: List[str]
        """

        self._embedded_urls = embedded_urls

    @property
    def image_urls(self) -> List[str]:
        """Gets the image_urls of this Message.


        :return: The image_urls of this Message.
        :rtype: List[str]
        """
        return self._image_urls

    @image_urls.setter
    def image_urls(self, image_urls: List[str]):
        """Sets the image_urls of this Message.


        :param image_urls: The image_urls of this Message.
        :type image_urls: List[str]
        """

        self._image_urls = image_urls

    @property
    def data_tags(self) -> List[str]:
        """Gets the data_tags of this Message.


        :return: The data_tags of this Message.
        :rtype: List[str]
        """
        return self._data_tags

    @data_tags.setter
    def data_tags(self, data_tags: List[str]):
        """Sets the data_tags of this Message.


        :param data_tags: The data_tags of this Message.
        :type data_tags: List[str]
        """

        self._data_tags = data_tags

    @property
    def annotations(self) -> List[Annotation]:
        """Gets the annotations of this Message.


        :return: The annotations of this Message.
        :rtype: List[Annotation]
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations: List[Annotation]):
        """Sets the annotations of this Message.


        :param annotations: The annotations of this Message.
        :type annotations: List[Annotation]
        """

        self._annotations = annotations

    @property
    def extra_attributes(self) -> List[ExtraAttribute]:
        """Gets the extra_attributes of this Message.


        :return: The extra_attributes of this Message.
        :rtype: List[ExtraAttribute]
        """
        return self._extra_attributes

    @extra_attributes.setter
    def extra_attributes(self, extra_attributes: List[ExtraAttribute]):
        """Sets the extra_attributes of this Message.


        :param extra_attributes: The extra_attributes of this Message.
        :type extra_attributes: List[ExtraAttribute]
        """

        self._extra_attributes = extra_attributes
