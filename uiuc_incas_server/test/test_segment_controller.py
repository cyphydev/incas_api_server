# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from uiuc_incas_server.models.uiuc_segment_collection import UiucSegmentCollection  # noqa: E501
from uiuc_incas_server.models.uiuc_segment_collection_meta import UiucSegmentCollectionMeta  # noqa: E501
from uiuc_incas_server.test import BaseTestCase


class TestSegmentController(BaseTestCase):
    """SegmentController integration test stubs"""

    def test_segment_collection_id_delete(self):
        """Test case for segment_collection_id_delete

        
        """
        response = self.client.open(
            '/api/v1/segmentCollection/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_segment_collection_id_get(self):
        """Test case for segment_collection_id_get

        
        """
        response = self.client.open(
            '/api/v1/segmentCollection/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_segment_collection_id_put(self):
        """Test case for segment_collection_id_put

        
        """
        body = UiucSegmentCollectionMeta()
        response = self.client.open(
            '/api/v1/segmentCollection/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_segment_collection_list_get(self):
        """Test case for segment_collection_list_get

        
        """
        query_string = [('collection_name', 'collection_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/segmentCollection/list',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_segment_collection_post(self):
        """Test case for segment_collection_post

        
        """
        body = UiucSegmentCollectionMeta()
        response = self.client.open(
            '/api/v1/segmentCollection',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
