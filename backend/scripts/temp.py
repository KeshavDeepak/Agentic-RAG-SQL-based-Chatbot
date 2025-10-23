import ast

from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri('sqlite:///backend/data/adventureworks.sqlite')

print(f"Dialect: {db.dialect}\n")
print(f"Available tables: {db.get_usable_table_names()}\n")

sample_query_output = ast.literal_eval(db.run("SELECT * FROM [Sales.Store] LIMIT 1;")) # type: ignore
print(f'Sample output: ')

for query in sample_query_output:
    print(query)
    print('\n')


print(db.run('PRAGMA table_info([Sales.Store])\n'))