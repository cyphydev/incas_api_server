from typing import List
from connexion.exceptions import OAuthProblem

import redis
from redis.commands.json.path import Path
from redis.exceptions import LockError
from uiuc_incas_server import util

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

@util.generic_db_lock_decor
def check_ApiKeyAuth(api_key, required_scopes):
    db_auth = util.get_db(db_name='auth')
    # with db_auth.lock('db_auth_lock', blocking_timeout=5) as lock:
    if not db_auth.json().type('apikeys', Path(f'{api_key}')):
        raise OAuthProblem('Invalid token')
    return db_auth.json().get('apikeys', Path(f'{api_key}'))
