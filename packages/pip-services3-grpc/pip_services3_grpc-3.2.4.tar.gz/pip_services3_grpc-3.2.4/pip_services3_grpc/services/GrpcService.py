# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import List, Any, Optional, Callable

from grpc import ServicerContext
from pip_services3_commons.config.ConfigParams import ConfigParams
from pip_services3_commons.config.IConfigurable import IConfigurable
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.errors.InvalidStateException import InvalidStateException
from pip_services3_commons.refer.DependencyResolver import DependencyResolver
from pip_services3_commons.refer.IReferences import IReferences
from pip_services3_commons.refer.IUnreferenceable import IUnreferenceable
from pip_services3_commons.run.IOpenable import IOpenable
from pip_services3_commons.validate import Schema
from pip_services3_components.count.CompositeCounters import CompositeCounters
from pip_services3_components.log.CompositeLogger import CompositeLogger
from pip_services3_components.trace.CompositeTracer import CompositeTracer
from pip_services3_rpc.services.InstrumentTiming import InstrumentTiming

from pip_services3_grpc.protos.commandable_pb2 import InvokeRequest
from .GrpcEndpoint import GrpcEndpoint
from .IRegisterable import IRegisterable


class GrpcService(IOpenable, IConfigurable, IRegisterable, IUnreferenceable):
    """
    Abstract service that receives remove calls via GRPC protocol.

    ### Configuration parameters ###
        - dependencies:
          - endpoint:              override for GRPC Endpoint dependency
          - controller:            override for Controller dependency
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it
        - credential - the HTTPS credentials:
          - ssl_key_file:         the SSL private key in PEM
          - ssl_crt_file:         the SSL certificate in PEM
          - ssl_ca_file:          the certificate authorities (root cerfiticates) in PEM


    .. code-block:: python

        class MyGrpcService(GrpcService, my_data_pb2_grpc.MyDataServicer):
            __controller: IMyController
            ...
            def __init__(self):
                suoer().__init__('.. service name ...')
                self._dependency_resolver.put(
                    "controller",
                    Descriptor("mygroup","controller","*","*","1.0")
                )

            def add_servicer_to_server(self, server):
                my_data_pb2_grpc.add_MyDataServicer_to_server(self, server)

            def set_references(self, references):
                super().set_references(references)
                self._controller = this._dependency_resolver.get_required("controller")

            def __number_of_calls_interceptor(self, request: InvokeRequest, context: ServicerContext,
                                    next: Callable[[InvokeRequest, ServicerContext], Any]) -> Any:
                self.__number_of_calls += 1
                return next(request, context)

            def __method(request: InvokeRequest, context: ServicerContext):
                correlationId = request.correlationId
                id = request.id
                return self._controller.get_my_data(correlationId, id)

            def register(self):

                self._register_interceptor(self.__number_of_calls_interceptor)
                self._register_method("get_mydata", None, method)
                
                self._register_service(self)
                ...



        service = MyGrpcService()
        service.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))

        service.set_references(References.from_tuples(
           Descriptor("mygroup","controller","default","default","1.0"), controller
        ))

        service.open("123")

    """

    __default_config = ConfigParams.from_tuples("dependencies.endpoint", "*:endpoint:grpc:*:1.0")

    def __init__(self, service_name: str = None):
        """
        Creates a new instance of the service.

        :param service_name: a service name.
        """
        self.__config: ConfigParams = None
        self.__references: IReferences = None
        self.__local_endpoint: bool = None
        self.__implementation: Any = {}
        self.__interceptors: List[Any] = []
        self.__opened: bool = None

        # The GRPC endpoint that exposes this service.
        self._endpoint: GrpcEndpoint = None

        # The dependency resolver.
        self._dependency_resolver = DependencyResolver(GrpcService.__default_config)

        # The logger.
        self._logger = CompositeLogger()

        # The performance counters.
        self._counters = CompositeCounters()

        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()

        self.__service_name: str = service_name
        self.__registrable = lambda implementation: self.__register_service(implementation)

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.
        :param config: configuration parameters to be set.
        """

        config = config.set_defaults(GrpcService.__default_config)
        self.__config = config
        self._dependency_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to this endpoint's logger, counters, and connection resolver.
        
        ### References ###
            - logger: **"\*:logger:\*:\*:1.0"**
            - counters: **"\*:counters:\*:\*:1.0"**
            - discovery: **"\*:discovery:\*:\*:1.0"** (for the connection resolver)

        :param references: an IReferences object, containing references to a logger, counters, and a connection resolver.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._tracer.set_references(references)
        self._dependency_resolver.set_references(references)

        # Get endpoint
        self._endpoint = self._dependency_resolver.get_one_optional('endpoint')

        # Or create a local one
        if self._endpoint is None:
            self._endpoint = self.__create_endpoint()
            self.__local_endpoint = True
        else:
            self.__local_endpoint = False

        #  Add registration callback to the endpoint
        self._endpoint.register(self)  # TODO check this

    def unset_references(self):
        """
        Unsets (clears) previously set references to dependent components.
        """
        # Remove registration callback from endpoint
        if self._endpoint is not None:
            self._endpoint.unregister(self)  # TODO check this
            self._endpoint = None

    def __create_endpoint(self) -> GrpcEndpoint:
        endpoint = GrpcEndpoint()

        if self.__config:
            endpoint.configure(self.__config)
        if self.__references:
            endpoint.set_references(self.__references)

        return endpoint

    def _instrument(self, correlation_id: Optional[str], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: CounterTiming object to end the time measurement.
        """
        self._logger.trace(correlation_id, 'Executing {} method'.format(name))
        self._counters.increment_one(name + '.exec_time')

        counter_timing = self._counters.begin_timing(name + '.exec_time')
        trace_timing = self._tracer.begin_trace(correlation_id, name, None)
        return InstrumentTiming(correlation_id, name, 'exec', self._logger, self._counters, counter_timing,
                                trace_timing)

    def _instrument_error(self, correlation_id: Optional[str], name: str, err: Exception, reerror=False):
        """
        Adds instrumentation to error handling.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :param err: an occured error
        :param reerror: if true - throw error
        """
        if err is not None:
            self._logger.error(correlation_id, err, 'Failed to execute {} method'.format(name))
            self._counters.increment_one(name + '.exec_errors')

        if reerror:
            raise err

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def open(self, correlation_id: Optional[str]):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """

        if self.__opened:
            return None

        if self._endpoint is None:
            self._endpoint = self.__create_endpoint()
            self._endpoint.register(self)
            self.__local_endpoint = True

        if self.__local_endpoint:
            try:
                self._endpoint.open(correlation_id)
                self.__opened = True
            except Exception as ex:
                self.__opened = False
                raise ex
        else:
            self.__opened = True

    def close(self, correlation_id: Optional[str]):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        if not self.__opened:
            return None

        if self._endpoint is None:
            raise InvalidStateException(correlation_id, 'NO_ENDPOINT', 'GRPC endpoint is missing')

        if self.__local_endpoint:
            self._endpoint.close(correlation_id)

        self.__opened = False

    def __register_service(self, implementation: 'GrpcService'):
        # self.register()
        implementation.__dict__.update(self.__implementation)
        if self._endpoint is not None:
            self._endpoint.register_service(implementation)

    def _apply_validation(self, schema: Schema, action: Callable[[InvokeRequest, ServicerContext], Any]) -> Callable[
        [InvokeRequest, ServicerContext], Any]:
        # Create an action function
        def action_wrapper(request: InvokeRequest, context: ServicerContext):
            # Validate object
            if schema and request:
                value = request
                if hasattr(value, 'to_object') and callable(value.to_object):
                    value = value.to_object()

                # Hack validation for filter and paging params
                validate_object = {}
                if hasattr(value, 'filter'):
                    validate_object['filter'] = FilterParams()
                    validate_object['filter'].update(value.filter)
                if hasattr(value, 'paging'):
                    validate_object['paging'] = PagingParams(value.paging.skip,
                                                             value.paging.take,
                                                             value.paging.total)
                if validate_object:
                    validate_object = type('ValidObject', (object,), validate_object)

                # Perform validation
                correlation_id = value.correlation_id
                schema.validate_and_throw_exception(correlation_id, validate_object or value, False)

            return action(request, context)

        return action_wrapper

    def _apply_interceptors(self, action: Callable[[InvokeRequest, ServicerContext], Any]) -> Callable[
        [InvokeRequest, ServicerContext], Any]:
        action_wrapper = action

        for index in reversed(range(len(self.__interceptors))):
            interceptor = self.__interceptors[index]
            wrap = lambda action: lambda request, context: interceptor(request, context, action)
            action_wrapper = wrap(action_wrapper)

        return action_wrapper

    def _register_method(self, name: str, schema: Schema, action: Callable[[InvokeRequest, ServicerContext], Any]):
        """
        Registers a method in GRPC service.

        :param name: a method name
        :param schema: a validation schema to validate received parameters.
        :param action: an action function that is called when operation is invoked.
        """
        if self.__implementation is None: return

        action_wrapper = self._apply_validation(schema, action)
        action_wrapper = self._apply_interceptors(action_wrapper)

        # Assign method implementation
        self.__implementation[name] = lambda request, context: action_wrapper(request, context)

    def _register_method_with_auth(self, name: str, schema: Schema,
                                   authorize: Callable[[InvokeRequest, ServicerContext, Callable], Any],
                                   action: Callable[[InvokeRequest, ServicerContext, Callable], Any]):
        """
        Registers a method with authorization.

        :param name: a method name
        :param schema: a validation schema to validate received parameters.
        :param authorize: an authorization interceptor
        :param action: an action function that is called when operation is invoked.
        """

        action_wrapper = self._apply_validation(schema, action)
        # Add authorization just before validation
        action_wrapper = lambda request, context: authorize(request, context, action_wrapper)
        action_wrapper = self._apply_interceptors(action_wrapper)

        # Assign method implementation
        self.__implementation[name] = lambda request, context: action_wrapper(request, context)

    def _register_interceptor(self, action: Callable[[InvokeRequest, ServicerContext, Callable], Any]):
        """
        Registers a middleware for methods in GRPC endpoint.

        :param action: an action function that is called when middleware is invoked.
        """
        if self._endpoint is not None:
            self.__interceptors.append(lambda request, context, next: action(request, context, next))

    @abstractmethod
    def register(self):
        """
        Registers all service routes in Grpc endpoint.
        This method is called by the service and must be overriden
        in child classes.
        """
