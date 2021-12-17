# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.actor_actor_graph import ActorActorGraph  # noqa: E501
from swagger_server.models.actor_message_graph import ActorMessageGraph  # noqa: E501
from swagger_server.models.message_message_graph import MessageMessageGraph  # noqa: E501
from swagger_server.models.uiuc_actor import UiucActor  # noqa: E501
from swagger_server.models.uiuc_message import UiucMessage  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGraphController(BaseTestCase):
    """GraphController integration test stubs"""

    def test_actor_actor_graph_get(self):
        """Test case for actor_actor_graph_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorActorGraph',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_actor_graph_id_delete(self):
        """Test case for actor_actor_graph_id_delete

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorActorGraph/{id}'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_actor_graph_id_get(self):
        """Test case for actor_actor_graph_id_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorActorGraph/{id}'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_actor_graph_id_neighbor_get(self):
        """Test case for actor_actor_graph_id_neighbor_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('graph_type', 'graph_type_example'),
                        ('version', 'version_example'),
                        ('actor_id', 'actor_id_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorActorGraph/{id}/neighbor'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_actor_graph_id_put(self):
        """Test case for actor_actor_graph_id_put

        
        """
        body = ActorActorGraph()
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorActorGraph/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_actor_graph_post(self):
        """Test case for actor_actor_graph_post

        
        """
        body = [ActorActorGraph()]
        response = self.client.open(
            '/incas/incas/1.0.0/actorActorGraph',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_message_graph_get(self):
        """Test case for actor_message_graph_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorMessageGraph',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_message_graph_id_delete(self):
        """Test case for actor_message_graph_id_delete

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorMessageGraph/{id}'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_message_graph_id_get(self):
        """Test case for actor_message_graph_id_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorMessageGraph/{id}'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_message_graph_id_neighbor_get(self):
        """Test case for actor_message_graph_id_neighbor_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('graph_type', 'graph_type_example'),
                        ('version', 'version_example'),
                        ('message_id', 'message_id_example'),
                        ('actor_id', 'actor_id_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorMessageGraph/{id}/neighbor'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_message_graph_id_put(self):
        """Test case for actor_message_graph_id_put

        
        """
        body = ActorMessageGraph()
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/actorMessageGraph/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_actor_message_graph_post(self):
        """Test case for actor_message_graph_post

        
        """
        body = [ActorMessageGraph()]
        response = self.client.open(
            '/incas/incas/1.0.0/actorMessageGraph',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_message_graph_get(self):
        """Test case for message_message_graph_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/messageMessageGraph',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_message_graph_id_delete(self):
        """Test case for message_message_graph_id_delete

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/messageMessageGraph/{id}'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_message_graph_id_get(self):
        """Test case for message_message_graph_id_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/messageMessageGraph/{id}'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_message_graph_id_neighbor_get(self):
        """Test case for message_message_graph_id_neighbor_get

        
        """
        query_string = [('provider_name', 'provider_name_example'),
                        ('graph_type', 'graph_type_example'),
                        ('version', 'version_example'),
                        ('message_id', 'message_id_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/messageMessageGraph/{id}/neighbor'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_message_graph_id_put(self):
        """Test case for message_message_graph_id_put

        
        """
        body = MessageMessageGraph()
        query_string = [('provider_name', 'provider_name_example'),
                        ('time_stamp', 'time_stamp_example'),
                        ('version', 'version_example')]
        response = self.client.open(
            '/incas/incas/1.0.0/messageMessageGraph/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_message_message_graph_post(self):
        """Test case for message_message_graph_post

        
        """
        body = [MessageMessageGraph()]
        response = self.client.open(
            '/incas/incas/1.0.0/messageMessageGraph',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
