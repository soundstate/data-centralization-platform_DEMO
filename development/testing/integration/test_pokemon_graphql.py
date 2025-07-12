# development/testing/integration/test_pokemon_graphql.py

import pytest
import asyncio
import sys
from pathlib import Path

# Add the packages directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages"))

from shared_core.api.clients.pokemon.pokemon_graphql_client import PokemonGraphQLClient


@pytest.mark.asyncio
async def test_pokemon_correlation_query():
    """Test Pokemon GraphQL API client with species query (based on working Postman query)"""
    client = PokemonGraphQLClient()
    
    try:
        # Use the method based on the working Postman query
        response = await client.get_pokemon_species_by_generation("generation-iii", limit=10)
        
        # Check response structure
        assert response is not None
        assert hasattr(response, 'success')
        assert hasattr(response, 'data')
        
        # Print response details for debugging
        print(f"Response success: {response.success}")
        print(f"Response status code: {response.status_code}")
        if response.errors:
            print(f"Response errors: {response.errors}")
        if response.data:
            print(f"Response data keys: {list(response.data.keys())}")
            if 'gen_species' in response.data:
                print(f"Gen III species count: {len(response.data['gen_species'])}")
        
        # Basic assertions
        assert response.success, f"API call failed: {response.errors}"
        assert response.data is not None, "Response data is None"
        assert "gen_species" in response.data, f"gen_species key missing from response. Keys: {list(response.data.keys())}"
        assert len(response.data["gen_species"]) == 10, f"Expected 10 Pokemon species, got {len(response.data['gen_species'])}"
        
        # Test first pokemon species structure
        first_species = response.data["gen_species"][0]
        assert "id" in first_species, "Pokemon species missing id field"
        assert "name" in first_species, "Pokemon species missing name field"
        
        print(f"✅ Test passed! Retrieved {len(response.data['gen_species'])} Generation III Pokemon species")
        print(f"   First species: {first_species['name']} (ID: {first_species['id']})")
        
        # Check generation info if available
        if "generation_info" in response.data and response.data["generation_info"]:
            gen_info = response.data["generation_info"][0]
            total_count = gen_info.get("pokemon_species", {}).get("aggregate", {}).get("count", 0)
            print(f"   Total Generation III species: {total_count}")
        
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")
    
    finally:
        # Clean up
        if hasattr(client, 'gql_client'):
            await client.gql_client.close_async()
        if hasattr(client, 'client'):
            await client.client.aclose()
