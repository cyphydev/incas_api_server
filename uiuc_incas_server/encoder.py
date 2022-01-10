from connexion.apps.flask_app import FlaskJSONEncoder
import six

from uiuc_incas_server.util import serialize


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o):
        return serialize(o)
