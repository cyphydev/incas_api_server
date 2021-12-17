# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class GeoLocation(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, latitude: float=None, longitude: float=None):  # noqa: E501
        """GeoLocation - a model defined in Swagger

        :param latitude: The latitude of this GeoLocation.  # noqa: E501
        :type latitude: float
        :param longitude: The longitude of this GeoLocation.  # noqa: E501
        :type longitude: float
        """
        self.swagger_types = {
            'latitude': float,
            'longitude': float
        }

        self.attribute_map = {
            'latitude': 'latitude',
            'longitude': 'longitude'
        }
        self._latitude = latitude
        self._longitude = longitude

    @classmethod
    def from_dict(cls, dikt) -> 'GeoLocation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GeoLocation of this GeoLocation.  # noqa: E501
        :rtype: GeoLocation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def latitude(self) -> float:
        """Gets the latitude of this GeoLocation.


        :return: The latitude of this GeoLocation.
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float):
        """Sets the latitude of this GeoLocation.


        :param latitude: The latitude of this GeoLocation.
        :type latitude: float
        """

        self._latitude = latitude

    @property
    def longitude(self) -> float:
        """Gets the longitude of this GeoLocation.


        :return: The longitude of this GeoLocation.
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float):
        """Sets the longitude of this GeoLocation.


        :param longitude: The longitude of this GeoLocation.
        :type longitude: float
        """

        self._longitude = longitude
