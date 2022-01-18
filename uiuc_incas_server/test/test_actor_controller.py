# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from uiuc_incas_server.models.actor_batch_get_body import ActorBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichment import ActorEnrichment  # noqa: E501
from uiuc_incas_server.models.actor_enrichment_meta import ActorEnrichmentMeta  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_delete_body import ActorEnrichmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_get_body import ActorEnrichmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_enrichments_batch_validation_response import ActorEnrichmentsBatchValidationResponse  # noqa: E501
from uiuc_incas_server.models.actor_segment_collections import ActorSegmentCollections  # noqa: E501
from uiuc_incas_server.models.actor_segments_batch_delete_body import ActorSegmentsBatchDeleteBody  # noqa: E501
from uiuc_incas_server.models.actor_segments_batch_get_body import ActorSegmentsBatchGetBody  # noqa: E501
from uiuc_incas_server.models.actor_segments_batch_validation_response import ActorSegmentsBatchValidationResponse  # noqa: E501
from uiuc_incas_server.models.uiuc_actor import UiucActor  # noqa: E501
from uiuc_incas_server.models.uiuc_segment_collection_meta import UiucSegmentCollectionMeta  # noqa: E501
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
        query_string = [('media_type', 'media_type_example'),
                        ('entity_type', 'entity_type_example')]
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

    def test_actor_enrichments_batch_delete_validate(self):
        """Test case for actor_enrichments_batch_delete_validate

        
        """
        body = ActorEnrichmentsBatchDeleteBody()
        response = self.client.open(
            '/api/v1/actor/enrichments/batchDelete/validate',
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

    def test_actor_enrichments_batch_post_validate(self):
        """Test case for actor_enrichments_batch_post_validate

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/enrichments/batch/validate',
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

    def test_actor_enrichments_batch_put_validate(self):
        """Test case for actor_enrichments_batch_put_validate

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/enrichments/batch/validate',
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
                        ('with_segment', true),
                        ('enrichment_name', 'enrichment_name_example'),
                        ('enrichment_provider_name', 'enrichment_provider_name_example'),
                        ('enrichment_version', 'enrichment_version_example'),
                        ('collection_name', 'collection_name_example'),
                        ('collection_provider_name', 'collection_provider_name_example'),
                        ('collection_version', 'collection_version_example'),
                        ('dev', true)]
        response = self.client.open(
            '/api/v1/actor/{id}'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_segments_delete(self):
        """Test case for actor_id_segments_delete

        
        """
        query_string = [('collection_name', 'collection_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/actor/{id}/segments'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_segments_get(self):
        """Test case for actor_id_segments_get

        
        """
        query_string = [('collection_name', 'collection_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example'),
                        ('dev', true)]
        response = self.client.open(
            '/api/v1/actor/{id}/segments'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_segments_post(self):
        """Test case for actor_id_segments_post

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/{id}/segments'.format(id='id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_id_segments_put(self):
        """Test case for actor_id_segments_put

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/{id}/segments'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_list_get(self):
        """Test case for actor_list_get

        
        """
        query_string = [('begin', 56),
                        ('end', 56),
                        ('media_type', 'media_type_example'),
                        ('entity_type', 'entity_type_example')]
        response = self.client.open(
            '/api/v1/actor/list',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segment_batch_delete(self):
        """Test case for actor_segment_batch_delete

        
        """
        body = ActorSegmentsBatchDeleteBody()
        response = self.client.open(
            '/api/v1/actor/segments/batchDelete',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_batch_delete_validate(self):
        """Test case for actor_segments_batch_delete_validate

        
        """
        body = ActorSegmentsBatchDeleteBody()
        response = self.client.open(
            '/api/v1/actor/segments/batchDelete/validate',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_batch_get(self):
        """Test case for actor_segments_batch_get

        
        """
        body = ActorSegmentsBatchGetBody()
        response = self.client.open(
            '/api/v1/actor/segments/batchGet',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_batch_post(self):
        """Test case for actor_segments_batch_post

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/segments/batch',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_batch_post_validate(self):
        """Test case for actor_segments_batch_post_validate

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/segments/batch/validate',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_batch_put(self):
        """Test case for actor_segments_batch_put

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/segments/batch',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_batch_put_validate(self):
        """Test case for actor_segments_batch_put_validate

        
        """
        body = None
        response = self.client.open(
            '/api/v1/actor/segments/batch/validate',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_meta_delete(self):
        """Test case for actor_segments_meta_delete

        
        """
        query_string = [('collection_name', 'collection_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/actor/segments/meta',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_meta_get(self):
        """Test case for actor_segments_meta_get

        
        """
        query_string = [('collection_name', 'collection_name_example'),
                        ('provider_name', 'provider_name_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/api/v1/actor/segments/meta',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_meta_post(self):
        """Test case for actor_segments_meta_post

        
        """
        body = UiucSegmentCollectionMeta()
        response = self.client.open(
            '/api/v1/actor/segments/meta',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_segments_meta_put(self):
        """Test case for actor_segments_meta_put

        
        """
        body = UiucSegmentCollectionMeta()
        response = self.client.open(
            '/api/v1/actor/segments/meta',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
