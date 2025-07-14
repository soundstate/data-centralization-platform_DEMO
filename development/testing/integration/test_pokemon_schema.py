# development/testing/integration/test_pokemon_schema.py

import asyncio
import sys
from pathlib import Path

import pytest

# Add the packages directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages"))

from gql import Client, gql
from gql.transport.httpx import HTTPXAsyncTransport


@pytest.mark.asyncio
async def test_pokemon_schema_exploration():
    """Test to explore Pokemon GraphQL schema"""

    # Initialize GraphQL client
    transport = HTTPXAsyncTransport(url="https://graphql.pokeapi.co/v1beta2")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    try:
        # First try a simple query to see what's available
        simple_query = gql(
            """
            query {
                __type(name: "Query") {
                    name
                    fields {
                        name
                        type {
                            name
                        }
                    }
                }
            }
        """,
        )

        result = await client.execute_async(simple_query)
        print("Available Query fields:")
        for field in result["__type"]["fields"]:
            print(f"  - {field['name']}")

        # Now let's try to find pokemon-related fields
        pokemon_fields = [
            f for f in result["__type"]["fields"] if "pokemon" in f["name"].lower()
        ]
        print(f"\nPokemon-related fields ({len(pokemon_fields)}):")
        for field in pokemon_fields:
            print(f"  - {field['name']}")

        # Test a simple pokemon query
        if pokemon_fields:
            first_pokemon_field = pokemon_fields[0]["name"]
            print(f"\nTesting query with field: {first_pokemon_field}")

            test_query = gql(
                f"""
                query {{
                    {first_pokemon_field}(limit: 5) {{
                        id
                        name
                    }}
                }}
            """,
            )

            test_result = await client.execute_async(test_query)
            print(
                f"✅ Query successful! Retrieved {len(test_result[first_pokemon_field])} items"
            )
            print(f"   First item: {test_result[first_pokemon_field][0]}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        pytest.fail(f"Schema exploration failed: {str(e)}")

    finally:
        await client.close_async()
