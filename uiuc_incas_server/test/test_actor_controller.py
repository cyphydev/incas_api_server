# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from uiuc_incas_server.models.actor_batch_get_body import ActorBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichment import ActorEnrichment  # noqa: E501
from uiuc_incas_server.models.actor_enrichment_meta import ActorEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_delete_body import ActorEnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_get_body import ActorEnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.uiuc_actor import UiucActor  # noqa: E501
from uiuc_incas_server.test import BaseTestCase


class TestActorController(BaseTestCase):
    """ActorController integration test stubs"""

    def test_actor_batch_get(self):
        """Test case for actor_batch_get

        
        """
        body = ActorBatchGetBody()
        response = self.client.open(
            '/api/v1/actor/batchGet',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_count_get(self):
        """Test case for actor_count_get

        
        """
        query_string = [('entity_type', 'entity_type_example')]
        response = self.client.open(
            '/api/v1/actor/count',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_batch_delete(self):
        """Test case for actor_enrichments_batch_delete

        
        """
        body = ActorEnrichmentsBatchDeleteBody()
        response = self.client.open(
            '/api/v1/actor/enrichments/batchDelete',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_batch_get(self):
        """Test case for actor_enrichments_batch_get

        
        """
        body = ActorEnrichmentsBatchGetBody()
        response = self.client.open(
            '/api/v1/actor/enrichments/batchGet',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_batch_post(self):
        """Test case for actor_enrichments_batch_post

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/enrichments/batch',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_batch_put(self):
        """Test case for actor_enrichments_batch_put

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/enrichments/batch',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_meta_delete(self):
        """Test case for actor_enrichments_meta_delete

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/actor/enrichments/meta',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_meta_get(self):
        """Test case for actor_enrichments_meta_get

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/actor/enrichments/meta',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_meta_post(self):
        """Test case for actor_enrichments_meta_post

        
        """
        body = ActorEnrichmentMeta()
        response = self.client.open(
            '/api/v1/actor/enrichments/meta',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_enrichments_meta_put(self):
        """Test case for actor_enrichments_meta_put

        
        """
        body = ActorEnrichmentMeta()
        response = self.client.open(
            '/api/v1/actor/enrichments/meta',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_enrichments_delete(self):
        """Test case for actor_id_enrichments_delete

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/actor/{id}/enrichments'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_enrichments_get(self):
        """Test case for actor_id_enrichments_get

        
        """
        query_string = [('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example'),
                        ('dev', true)]
        response = self.client.open(
            '/api/v1/actor/{id}/enrichments'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_enrichments_post(self):
        """Test case for actor_id_enrichments_post

        
        """
        body = ActorEnrichment()
        response = self.client.open(
            '/api/v1/actor/{id}/enrichments'.format(id='id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_enrichments_put(self):
        """Test case for actor_id_enrichments_put

        
        """
        body = ActorEnrichment()
        response = self.client.open(
            '/api/v1/actor/{id}/enrichments'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_get(self):
        """Test case for actor_id_get

        
        """
        query_string = [('with_enrichment', true),
                        ('enrichment_name', 'enrichment_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example'),
                        ('dev', true)]
        response = self.client.open(
            '/api/v1/actor/{id}'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_list_get(self):
        """Test case for actor_list_get

        
        """
        query_string = [('begin', 56),
                        ('end', 56),
                        ('entity_type', 'entity_type_example')]
        response = self.client.open(
            '/api/v1/actor/list',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
