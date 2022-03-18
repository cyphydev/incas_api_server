#!/usr/bin/env python3

import os
import connexion

from uiuc_incas_server import encoder, util


def main():
    db_auth = util.get_db('auth')
    if not db_auth.exists('apikeys'):
        print('Creating apikeys key')
        db_auth.json().set('apikeys', '$', {os.environ['UIUC_INCAS_API_KEY']: {'user':' admin', 'scope': {'admin': True}}})
    else:
        print('apikeys exists in DB')

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'INCAS TA2-UIUC Datatypes'}, pythonic_params=True)
    app.run(host='0.0.0.0',
            port=os.environ.get('INCAS_SRV_PORT', '8443'),
            ssl_context=(os.environ['INCAS_SRV_CERT_PATH'],
                         os.environ['INCAS_SRV_KEY_PATH']))


if __name__ == '__main__':
    main()
