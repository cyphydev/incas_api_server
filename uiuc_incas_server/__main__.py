#!/usr/bin/env python3

import connexion

from uiuc_incas_server import encoder


def main():
    app = connexion.FlaskApp(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'INCAS TA2-UIUC Datatypes'}, strict_validation=True, pythonic_params=True)
    app.run(port=8443)


if __name__ == '__main__':
    main()
