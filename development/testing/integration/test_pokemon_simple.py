# development/testing/integration/test_pokemon_simple.py

import asyncio
import sys
from pathlib import Path

import pytest

# Add the packages directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages"))

from gql import Client, gql
from gql.transport.httpx import HTTPXAsyncTransport


@pytest.mark.asyncio
async def test_pokemon_simple_query():
    """Test a simple working Pokemon GraphQL query"""

    # Initialize GraphQL client
    transport = HTTPXAsyncTransport(url="https://graphql.pokeapi.co/v1beta2")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    try:
        # Based on the error, let's try different field names
        possible_queries = [
            # Try the suggested field
            gql(
                """
                query {
                    pokemonevolution(limit: 5) {
                        id
                        name
                    }
                }
            """,
            ),
            # Try standard pokemon field
            gql(
                """
                query {
                    pokemon(limit: 5) {
                        id
                        name
                    }
                }
            """,
            ),
            # Try with v2 suffix
            gql(
                """
                query {
                    pokemon_v2(limit: 5) {
                        id
                        name
                    }
                }
            """,
            ),
            # Try without suffix
            gql(
                """
                query {
                    pokemons(limit: 5) {
                        id
                        name
                    }
                }
            """,
            ),
        ]

        for i, query in enumerate(possible_queries):
            try:
                print(f"\n🔍 Testing query {i+1}...")
                result = await client.execute_async(query)
                print(f"✅ Query {i+1} successful!")
                print(f"   Result keys: {list(result.keys())}")

                # Print the first few results
                for key, value in result.items():
                    if isinstance(value, list) and len(value) > 0:
                        print(f"   {key}: {len(value)} items")
                        print(f"   First item: {value[0]}")
                        break

                # If successful, stop testing
                break

            except Exception as e:
                print(f"❌ Query {i+1} failed: {str(e)[:100]}...")
                continue

    except Exception as e:
        print(f"❌ Setup Error: {str(e)}")
        pytest.fail(f"Test setup failed: {str(e)}")

    finally:
        await client.close_async()
