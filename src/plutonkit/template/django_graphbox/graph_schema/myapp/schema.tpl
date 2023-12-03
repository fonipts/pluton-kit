from django_graphbox.builder import SchemaBuilder
from graph_schema.myapp.models import MyModel

builder = SchemaBuilder()
builder.add_model(MyModel)
query_class = builder.build_schema_query()
mutation_class = builder.build_schema_mutation()
