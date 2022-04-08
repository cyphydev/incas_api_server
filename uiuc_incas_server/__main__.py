#!/usr/bin/env python3

import os
import connexion
import logging
from retry import retry

import redis
from redis.commands.json.path import Path

from uiuc_incas_server import encoder, util

logger = logging.getLogger('uiuc_incas_server')

@retry(redis.exceptions.BusyLoadingError, delay=1, backoff=2, max_delay=4)
def check_api_key():
    db_auth = util.get_db('auth')
    if not db_auth.exists('apikeys'):
        logger.info('Creating apikeys key')
        db_auth.json().set('apikeys', Path.rootPath(), {os.environ['UIUC_INCAS_API_KEY']: {'user':' admin', 'scope': {'admin': True}}})
    else:
        logger.info('apikeys exists in DB')

def main():
    check_api_key()

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'INCAS TA2-UIUC Datatypes'}, pythonic_params=True)
    app.run(host='0.0.0.0',
            port=os.environ.get('INCAS_SRV_PORT', '8443'),
            ssl_context=(os.environ['INCAS_SRV_CERT_PATH'],
                         os.environ['INCAS_SRV_KEY_PATH']))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
