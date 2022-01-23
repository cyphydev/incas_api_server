# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from uiuc_incas_server.models.uiuc_actor import UiucActor  # noqa: E501
from uiuc_incas_server.models.uiuc_message import UiucMessage  # noqa: E501
from uiuc_incas_server.test import BaseTestCase


class TestAdminController(BaseTestCase):
    """AdminController integration test stubs"""

    def test_admin_actor_post(self):
        """Test case for admin_actor_post

        
        """
        body = [UiucActor()]
        response = self.client.open(
            '/api/v1/actor',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_message_post(self):
        """Test case for admin_message_post

        
        """
        body = [UiucMessage()]
        response = self.client.open(
            '/api/v1/message',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
