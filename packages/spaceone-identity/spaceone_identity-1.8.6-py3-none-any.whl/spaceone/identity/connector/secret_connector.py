"""
Deprecated:
  Not used. Integrated with SpaceConnector.
"""

import logging

from spaceone.core.connector import BaseConnector
from google.protobuf.json_format import MessageToDict
from spaceone.core import pygrpc
from spaceone.core.utils import parse_endpoint
from spaceone.core.error import *

__all__ = ['SecretConnector']
_LOGGER = logging.getLogger(__name__)


class SecretConnector(BaseConnector):
    def __init__(self, transaction, config):
        super().__init__(transaction, config)

        if 'endpoint' not in self.config:
            raise ERROR_WRONG_CONFIGURATION(key='endpoint')

        if len(self.config['endpoint']) > 1:
            raise ERROR_WRONG_CONFIGURATION(key='too many endpoint')

        for (k, v) in self.config['endpoint'].items():
            e = parse_endpoint(v)
            self.client = pygrpc.client(endpoint=f'{e.get("hostname")}:{e.get("port")}', version=k)

    def get(self, secret_id, domain_id):
        resp = self.client.Secret.get({'secret_id': secret_id, 'domain_id': domain_id},
                                      metadata=self.transaction.get_connection_meta())
        return MessageToDict(resp, preserving_proto_field_name=True)

    def get_data(self, secret_id, domain_id):
        resp = self.client.Secret.get_data({'secret_id': secret_id, 'domain_id': domain_id},
                                           metadata=self.transaction.get_connection_meta())
        return MessageToDict(resp, preserving_proto_field_name=True)

