import graphene
from graph_schema.myapp.schema import query_class, mutation_class

class Query(query_class, graphene.ObjectType):
    pass

class Mutation(mutation_class, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
