# main.py
from aiohttp import web
from tartiflette import Resolver
from tartiflette_aiohttp import register_graphql_handlers
({SQL_ALCH_IMPORT})

@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]

sdl = """
    type Query {
        hello(name: String): String
    }
"""
({SQL_ALCH_DB_CONTENT})
web.run_app(
    register_graphql_handlers(
        web.Application(),
        engine_sdl=sdl
    )
)
