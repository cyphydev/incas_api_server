# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.message_enrichment import MessageEnrichment  # noqa: E501
from swagger_server.models.message_enrichment_meta import MessageEnrichmentMeta  # noqa: E501
from swagger_server.models.uiuc_message import UiucMessage  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMessageController(BaseTestCase):
    """MessageController integration test stubs"""

    def test_message_enrichments_delete(self):
        """Test case for message_enrichments_delete

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/message/enrichments',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_get(self):
        """Test case for message_enrichments_get

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/message/enrichments',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_post(self):
        """Test case for message_enrichments_post

        
        """
        body = [MessageEnrichmentMeta()]
        response = self.client.open(
            '/incas/incas/1.0.0/message/enrichments',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_put(self):
        """Test case for message_enrichments_put

        
        """
        body = [MessageEnrichmentMeta()]
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/message/enrichments',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_delete(self):
        """Test case for message_id_enrichments_delete

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/message/{id}/enrichments'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_get(self):
        """Test case for message_id_enrichments_get

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/message/{id}/enrichments'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_post(self):
        """Test case for message_id_enrichments_post

        
        """
        body = [MessageEnrichment()]
        response = self.client.open(
            '/incas/incas/1.0.0/message/{id}/enrichments'.format(id='id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_put(self):
        """Test case for message_id_enrichments_put

        
        """
        body = [MessageEnrichment()]
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/message/{id}/enrichments'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_get(self):
        """Test case for message_id_get

        
        """
        response = self.client.open(
            '/incas/incas/1.0.0/message/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
