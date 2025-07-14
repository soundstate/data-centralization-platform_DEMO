# development/testing/integration/test_pokemon_fields.py

import asyncio
import sys
from pathlib import Path

import pytest

# Add the packages directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages"))

from gql import Client, gql
from gql.transport.httpx import HTTPXAsyncTransport


@pytest.mark.asyncio
async def test_pokemon_fields_discovery():
    """Test to discover available fields on Pokemon type"""

    # Initialize GraphQL client
    transport = HTTPXAsyncTransport(url="https://graphql.pokeapi.co/v1beta2")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    try:
        # Discover Pokemon type fields
        schema_query = gql(
            """
            query {
                __type(name: "pokemon") {
                    name
                    fields {
                        name
                        type {
                            name
                            kind
                        }
                    }
                }
            }
        """
        )

        result = await client.execute_async(schema_query)

        if result["__type"]:
            print("Available Pokemon fields:")
            for field in result["__type"]["fields"]:
                print(
                    f"  - {field['name']}: {field['type']['name']} ({field['type']['kind']})",
                )
        else:
            print("Pokemon type not found. Let's try a simple working query:")

            # Try the simple working query
            simple_query = gql(
                """
                query {
                    pokemon(limit: 3) {
                        id
                        name
                        height
                        weight
                    }
                }
            """
            )

            simple_result = await client.execute_async(simple_query)
            print("✅ Simple query successful!")
            print(f"Retrieved {len(simple_result['pokemon'])} Pokemon:")
            for p in simple_result["pokemon"]:
                print(
                    f"  - {p['name']} (ID: {p['id']}, Height: {p['height']}, Weight: {p['weight']})",
                )

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        pytest.fail(f"Field discovery failed: {str(e)}")

    finally:
        await client.close_async()
