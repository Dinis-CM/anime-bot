import os

def load_query(query_name: str) -> str:
    base_dir = os.path.dirname(__file__)
    queries_dir = os.path.abspath(os.path.join(base_dir, "../queries/graphql_queries"))
    file_path = os.path.join(queries_dir, f"{query_name}.graphql")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()