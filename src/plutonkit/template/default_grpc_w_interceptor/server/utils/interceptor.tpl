
import grpc



class AuthenticationInterceptor:
    def __init__(self, header, value, code, details):
        self._header = header
        self._value = value
        self._terminator = self._unary_unary_rpc_terminator(code, details)

    def _unary_unary_rpc_terminator(self,code, details):

        def terminate(ignored_request, context):
            context.abort(code, details)

        return grpc.unary_unary_rpc_method_handler(terminate)

    def intercept_service(self, continuation, handler_call_details):
        if (self._header,
                self._value) in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._terminator
