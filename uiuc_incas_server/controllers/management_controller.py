import connexion
import six

from uiuc_incas_server import util


def ping_get():  # noqa: E501
    """ping_get

    Ping the server # noqa: E501


    :rtype: None
    """
    return 'Pong', 200
