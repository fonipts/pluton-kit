"""Module providing a function printing python version."""

from plutonkit.management.format import format_argument_input
from plutonkit.config.framework import (
    DEFAULT_GRPC,
    FRAMEWORK_WEB,
    DEFAULT_WEB_SOCKET,
    FRAMEWORK_GRAPHQL,
    DEFAULT_WEB3,
    DEFAULT_PACKAGE,
)

SERVICE_TYPE = [
    format_argument_input(
        "service_type", "grpc", "Your GRPC Framework", "grpc", DEFAULT_GRPC
    ),
    format_argument_input(
        "service_type", "web", "Your web framework choice", "web", FRAMEWORK_WEB
    ),
    format_argument_input(
        "service_type",
        "websocket",
        "Websocket Framework",
        "websocket",
        DEFAULT_WEB_SOCKET,
    ),
    format_argument_input(
        "service_type",
        "graphql",
        "Your GraphQl Framework",
        "graphql",
        FRAMEWORK_GRAPHQL,
    ),
    format_argument_input(
        "service_type", "web3", "Your Web3/blockain", "web3", DEFAULT_WEB3
    ),
    format_argument_input(
        "service_type",
        "packaging_app",
        "Your New packaging apps",
        "packaging_app",
        DEFAULT_PACKAGE,
    ),
]
