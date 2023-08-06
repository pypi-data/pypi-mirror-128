# -*- coding: utf-8 -*-

from typing import Optional

from pip_services3_commons.data.DataPage import DataPage
from pip_services3_commons.data.FilterParams import FilterParams
from pip_services3_commons.data.PagingParams import PagingParams

from pip_services3_grpc.clients.GrpcClient import GrpcClient
from .IDummyClient import IDummyClient
from ..Dummy import Dummy
from ..protos import dummies_pb2
from ..protos import dummies_pb2_grpc


class DummyGrpcClient(GrpcClient, IDummyClient):

    def __init__(self):
        super().__init__(dummies_pb2_grpc.DummiesStub, 'dummies.Dummies')

    def get_dummies(self, correlation_id: Optional[str], filter: FilterParams, paging: PagingParams) -> DataPage:
        request = dummies_pb2.DummiesPageRequest()
        request.correlation_id = correlation_id

        if filter is not None:
            request.filter.update(filter)

        if paging is not None:
            request.paging.total = paging.total
            request.paging.skip += paging.skip
            request.paging.take = paging.take

        self._instrument(correlation_id, 'dummy.get_page_by_filter')
        response = self._call('get_dummies', correlation_id, request)
        items = []
        for item in response.data:
            items.append(item)

        return DataPage(items, int(response.total))

    def get_dummy_by_id(self, correlation_id: Optional[str], dummy_id: str) -> Optional[Dummy]:
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = dummy_id

        self._instrument(correlation_id, 'dummy.get_one_by_id')
        response = self._call('get_dummy_by_id', correlation_id, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response

    def create_dummy(self, correlation_id: Optional[str], dummy: Dummy) -> Optional[Dummy]:
        request = dummies_pb2.DummyObjectRequest()
        request.correlation_id = correlation_id

        request.dummy.id = dummy.id
        request.dummy.key = dummy.key
        request.dummy.content = dummy.content

        self._instrument(correlation_id, 'dummy.create')

        response = self._call('create_dummy', correlation_id, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response

    def update_dummy(self, correlation_id: Optional[str], dummy: Dummy) -> Optional[Dummy]:
        request = dummies_pb2.DummyObjectRequest()
        request.correlation_id = correlation_id

        request.dummy.id = dummy.id
        request.dummy.key = dummy.key
        request.dummy.content = dummy.content

        self._instrument(correlation_id, 'dummy.update')

        response = self._call('update_dummy', correlation_id, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response

    def delete_dummy(self, correlation_id: Optional[str], dummy_id: str) -> Optional[Dummy]:
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = dummy_id

        self._instrument(correlation_id, 'dummy.delete')

        response = self._call('delete_dummy_by_id', correlation_id, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response
