from plutonkit.helper.format import format_argument
from plutonkit.config.framework import DEFAULT_GRPC,FRAMEWORK_WEB,DEFAULT_WEB_SOCKET,FRAMEWORK_GRAPHQL,DEFAULT_WEB3

SERVICE_TYPE = [
    format_argument("service_type","grpc","Your GRPC Framework","grpc",DEFAULT_GRPC),
    format_argument("service_type","web","Your web framework choice","web",FRAMEWORK_WEB),
    format_argument("service_type","websocket","Websocker GRPC Framework","websocket",DEFAULT_WEB_SOCKET),
    format_argument("service_type","graphql","Your GraphQl Framework","graphql",FRAMEWORK_GRAPHQL),
    format_argument("service_type","web3","Your Web3/blockain","web3",DEFAULT_WEB3),

]

