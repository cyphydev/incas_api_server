# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from uiuc_incas_server.models.message_batch_get_body import MessageBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_enrichment import MessageEnrichment  # noqa: E501
from uiuc_incas_server.models.message_enrichment_meta import MessageEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_delete_body import MessageEnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_delete_validation_response import MessageEnrichmentsBatchDeleteValidationResponse  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_get_body import MessageEnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.message_enrichments_batch_validation_response import MessageEnrichmentsBatchValidationResponse  # noqa: E501
from uiuc_incas_server.models.message_id_response import MessageIdResponse  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server.test import BaseTestCase


class TestMessageController(BaseTestCase):
    """MessageController integration test stubs"""

    def test_message_batch_get(self):
        """Test case for message_batch_get

        
        """
        body = MessageBatchGetBody()
        response = self.client.open(
            '/api/v1/message/batchGet',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_count_get(self):
        """Test case for message_count_get

        
        """
        query_string = [('media_type', 'media_type_example')]
        response = self.client.open(
            '/api/v1/message/count',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_batch_delete(self):
        """Test case for message_enrichments_batch_delete

        
        """
        body = MessageEnrichmentsBatchDeleteBody()
        response = self.client.open(
            '/api/v1/message/enrichments/batchDelete',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_batch_delete_validate(self):
        """Test case for message_enrichments_batch_delete_validate

        
        """
        body = MessageEnrichmentsBatchDeleteBody()
        response = self.client.open(
            '/api/v1/message/enrichments/batchDelete/validate',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_batch_get(self):
        """Test case for message_enrichments_batch_get

        
        """
        body = MessageEnrichmentsBatchGetBody()
        response = self.client.open(
            '/api/v1/message/enrichments/batchGet',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_batch_post(self):
        """Test case for message_enrichments_batch_post

        
        """
        body = None
        response = self.client.open(
            '/api/v1/message/enrichments/batch',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_batch_post_validate(self):
        """Test case for message_enrichments_batch_post_validate

        
        """
        body = None
        response = self.client.open(
            '/api/v1/message/enrichments/batch/validate',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_batch_put(self):
        """Test case for message_enrichments_batch_put

        
        """
        body = None
        response = self.client.open(
            '/api/v1/message/enrichments/batch',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_batch_put_validate(self):
        """Test case for message_enrichments_batch_put_validate

        
        """
        body = None
        response = self.client.open(
            '/api/v1/message/enrichments/batch/validate',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_meta_delete(self):
        """Test case for message_enrichments_meta_delete

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/message/enrichments/meta',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_meta_get(self):
        """Test case for message_enrichments_meta_get

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/message/enrichments/meta',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_meta_post(self):
        """Test case for message_enrichments_meta_post

        
        """
        body = MessageEnrichmentMeta()
        response = self.client.open(
            '/api/v1/message/enrichments/meta',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_enrichments_meta_put(self):
        """Test case for message_enrichments_meta_put

        
        """
        body = MessageEnrichmentMeta()
        response = self.client.open(
            '/api/v1/message/enrichments/meta',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_delete(self):
        """Test case for message_id_enrichments_delete

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/message/{id}/enrichments'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_get(self):
        """Test case for message_id_enrichments_get

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example'),
                        ('dev', true)]
        response = self.client.open(
            '/api/v1/message/{id}/enrichments'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_post(self):
        """Test case for message_id_enrichments_post

        
        """
        body = MessageEnrichment()
        response = self.client.open(
            '/api/v1/message/{id}/enrichments'.format(id='id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_enrichments_put(self):
        """Test case for message_id_enrichments_put

        
        """
        body = MessageEnrichment()
        response = self.client.open(
            '/api/v1/message/{id}/enrichments'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_id_get(self):
        """Test case for message_id_get

        
        """
        query_string = [('with_enrichment', true),
                        ('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example'),
                        ('dev', true)]
        response = self.client.open(
            '/api/v1/message/{id}'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_list_get(self):
        """Test case for message_list_get

        
        """
        query_string = [('begin', 56),
                        ('end', 56),
                        ('media_type', 'media_type_example')]
        response = self.client.open(
            '/api/v1/message/list',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
