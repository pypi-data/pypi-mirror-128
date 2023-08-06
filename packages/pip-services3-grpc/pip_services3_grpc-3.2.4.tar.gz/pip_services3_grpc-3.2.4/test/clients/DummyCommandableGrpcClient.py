# -*- coding: utf-8 -*-

from typing import Optional

from pip_services3_commons.data.DataPage import DataPage
from pip_services3_commons.data.FilterParams import FilterParams
from pip_services3_commons.data.PagingParams import PagingParams

from pip_services3_grpc.clients.CommandableGrpcClient import CommandableGrpcClient
from .IDummyClient import IDummyClient
from ..Dummy import Dummy
from ..protos import dummies_pb2_grpc


class DummyCommandableGrpcClient(CommandableGrpcClient, IDummyClient):

    def __init__(self):
        super().__init__('dummy')

    def get_dummies(self, correlation_id: Optional[str], filter: FilterParams, paging: PagingParams) -> DataPage:
        return self.call_command('get_dummies', correlation_id, {'filter': filter, 'paging': paging})

    def get_dummy_by_id(self, correlation_id: Optional[str], dummy_id) -> Dummy:
        return self.call_command('get_dummy_by_id', correlation_id, {'dummy_id': dummy_id})

    def create_dummy(self, correlation_id: Optional[str], dummy) -> Dummy:
        return self.call_command('create_dummy', correlation_id, {'dummy': dummy})

    def update_dummy(self, correlation_id: Optional[str], dummy) -> Dummy:
        return self.call_command('update_dummy', correlation_id, {'dummy': dummy})

    def delete_dummy(self, correlation_id: Optional[str], dummy_id: str) -> Dummy:
        return self.call_command('delete_dummy', correlation_id, {'dummy_id': dummy_id})
