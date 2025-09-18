"""Module providing a function printing python version."""

from plutonkit.config.framework import (
    DEFAULT_GRPC, DEFAULT_PACKAGE, DEFAULT_WEB3, DEFAULT_WEB_SOCKET,
    FRAMEWORK_GRAPHQL, FRAMEWORK_WEB,
)
from plutonkit.model.dataclass.format_argument_input import FormatArgumentInput

SERVICE_TYPE = [
    FormatArgumentInput(
        type="service_type", name="grpc", question="Your GRPC Framework", option_name="grpc", config=DEFAULT_GRPC
    ),
    FormatArgumentInput(
        type="service_type", name="web", question="Your web framework choice", option_name="web", config=FRAMEWORK_WEB
    ),
    FormatArgumentInput(
        type="service_type",
        name="websocket",
        question="Websocket Framework",
        option_name="websocket",
        config=DEFAULT_WEB_SOCKET,
    ),
    FormatArgumentInput(
        type="service_type",
        name="graphql",
        question="Your GraphQl Framework",
        option_name="graphql",
        config=FRAMEWORK_GRAPHQL,
    ),
    FormatArgumentInput(
        type="service_type", name="web3", question="Your Web3/blockain", option_name="web3", config=DEFAULT_WEB3
    ),
    FormatArgumentInput(
        type="service_type",
        name="language_starter",
        question="Your New Language starter",
        option_name="language_starter",
        config=DEFAULT_PACKAGE,
    ),
]
