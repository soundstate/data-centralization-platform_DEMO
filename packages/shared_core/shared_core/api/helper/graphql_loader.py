import importlib.resources
from functools import lru_cache


class GraphQLFileNotFound(Exception):
    pass


@lru_cache(maxsize=128)
def load_graphql_query(query_name: str, category: str = "items") -> str:
    """
    Load a GraphQL query from the package resources.

    Args:
        query_name (str): Name of the GraphQL file (without .graphql extension)
        category (str): Category folder (items, boards, mutations, etc.)

    Returns:
        str: Contents of the GraphQL query file

    Raises:
        GraphQLFileNotFound: If the file doesn't exist
    """
    try:
        # Use importlib.resources to access files within the package
        graphql_package = f"jobe_shared.api.saas.monday.graphql.{category}"
        filename = f"{query_name}.graphql"

        try:
            # Python 3.9+
            files = importlib.resources.files(graphql_package)
            query_file = files / filename
            if query_file.is_file():
                return query_file.read_text(encoding="utf-8")
        except AttributeError:
            # Python 3.8 fallback
            with importlib.resources.path(graphql_package, filename) as query_path:
                return query_path.read_text(encoding="utf-8")

        raise GraphQLFileNotFound(f"GraphQL file not found: {category}/{filename}")

    except Exception as e:
        raise GraphQLFileNotFound(
            f"Error loading GraphQL file {category}/{query_name}: {e}"
        )


@lru_cache(maxsize=128)
def load_graphql_query_from_path(relative_path: str) -> str:
    """
    Load GraphQL query using relative path within the package.
    For complex nested structures like gather_specific_item_details/

    Args:
        relative_path (str): Path relative to monday/graphql/ (e.g., "items/gather_specific_item_details/query.graphql")

    Returns:
        str: Contents of the GraphQL query file
    """
    try:
        base_package = "jobe_shared.api.saas.monday.graphql"

        # Split path into parts
        path_parts = relative_path.split("/")
        filename = path_parts[-1]
        package_path = ".".join(path_parts[:-1])

        full_package = (
            f"{base_package}.{package_path}" if package_path else base_package
        )

        try:
            # Python 3.9+
            files = importlib.resources.files(full_package)
            query_file = files / filename
            if query_file.is_file():
                return query_file.read_text(encoding="utf-8")
        except AttributeError:
            # Python 3.8 fallback
            with importlib.resources.path(full_package, filename) as query_path:
                return query_path.read_text(encoding="utf-8")

        raise GraphQLFileNotFound(f"GraphQL file not found: {relative_path}")

    except Exception as e:
        raise GraphQLFileNotFound(f"Error loading GraphQL file {relative_path}: {e}")
