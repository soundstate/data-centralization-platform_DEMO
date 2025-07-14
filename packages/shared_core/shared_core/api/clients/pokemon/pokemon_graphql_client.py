"""
Pokemon GraphQL API Client

Comprehensive client for Pokemon GraphQL API with:
- Type-based correlations for weather patterns
- Habitat data for geographic analysis
- Generation data for temporal trends
- Evolution chains for progression analysis
"""

from config.base_client import APIResponse, BaseAPIClient
from gql import Client, gql
from gql.transport.httpx import HTTPXAsyncTransport


class PokemonGraphQLClient(BaseAPIClient):
    """
    Pokemon GraphQL API client for correlation analysis
    """

    def __init__(
        self,
        api_url: str = "https://graphql.pokeapi.co/v1beta2",
        debug_mode: bool = True,
        **kwargs,
    ):
        """
        Initialize Pokemon GraphQL client
        """
        super().__init__(
            base_url=api_url,
            debug_mode=debug_mode,
            rate_limit_per_minute=100,
            client_name="pokemon_graphql",
            **kwargs,
        )

        # Initialize GraphQL client
        transport = HTTPXAsyncTransport(url=self.base_url)
        self.gql_client = Client(transport=transport, fetch_schema_from_transport=True)

        if self.debug_mode:
            self.logger.info("⚡ Initialized Pokemon GraphQL client")

    async def get_pokemon_for_correlation(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> APIResponse:
        """
        Get Pokemon data optimized for correlation analysis
        """
        query = gql(
            """
            query GetPokemonForCorrelation($limit: Int!, $offset: Int!) {
                pokemon(
                    limit: $limit,
                    offset: $offset
                ) {
                    id
                    name
                    height
                    weight
                    base_experience
                    order
                    pokemon_species_id
                    pokemontypes {
                        type {
                            id
                            name
                        }
                    }
                    pokemonspecy {
                        id
                        name
                        generation_id
                        evolution_chain_id
                    }
                    pokemonstats {
                        base_stat
                        stat {
                            id
                            name
                        }
                    }
                    pokemonabilities {
                        ability {
                            id
                            name
                            generation_id
                        }
                    }
                }
            }
        """
        )

        variables = {"limit": limit, "offset": offset}

        try:
            result = await self.gql_client.execute_async(query, variables)

            return APIResponse(
                data=result,
                success=True,
                status_code=200,
                response_time_ms=0,  # GraphQL client doesn't provide this
                metadata={
                    "total_count": result.get("pokemon_count", {})
                    .get("aggregate", {})
                    .get("count", 0),
                    "returned_count": len(result.get("pokemon", [])),
                    "offset": offset,
                },
            )
        except Exception as e:
            return APIResponse(
                success=False, status_code=500, response_time_ms=0, errors=[str(e)]
            )

    async def get_pokemon_by_type(self, type_name: str) -> APIResponse:
        """
        Get all Pokemon of a specific type (for weather correlations)
        """
        query = gql(
            """
            query GetPokemonByType($typeName: String!) {
                pokemon: pokemon_v2_pokemontype(
                    where: {
                        pokemon_v2_type: {name: {_eq: $typeName}}
                    }
                ) {
                    pokemon: pokemon_v2_pokemon {
                        id
                        name
                        species: pokemon_v2_pokemonspecy {
                            generation_id
                            habitat: pokemon_v2_pokemonhabitat {
                                name
                            }
                        }
                    }
                }
                
                type_info: pokemon_v2_type(where: {name: {_eq: $typeName}}) {
                    id
                    name
                    generation_id
                    damage_relations: pokemon_v2_typeefficacies {
                        damage_factor
                        target_type: pokemonV2TypeByTargetTypeId {
                            name
                        }
                    }
                }
            }
        """
        )

        variables = {"typeName": type_name}

        try:
            result = await self.gql_client.execute_async(query, variables)
            return APIResponse(
                data=result, success=True, status_code=200, response_time_ms=0
            )
        except Exception as e:
            return APIResponse(
                success=False, status_code=500, response_time_ms=0, errors=[str(e)]
            )

    async def get_pokemon_by_habitat(self, habitat_name: str) -> APIResponse:
        """
        Get Pokemon by habitat (for geographic correlations)
        """
        query = gql(
            """
            query GetPokemonByHabitat($habitatName: String!) {
                species: pokemon_v2_pokemonspecies(
                    where: {
                        pokemon_v2_pokemonhabitat: {name: {_eq: $habitatName}}
                    }
                ) {
                    id
                    name
                    generation_id
                    pokemon: pokemon_v2_pokemons {
                        id
                        name
                        types: pokemon_v2_pokemontypes {
                            type: pokemon_v2_type {
                                name
                            }
                        }
                    }
                }
                
                habitat_info: pokemon_v2_pokemonhabitat(
                    where: {name: {_eq: $habitatName}}
                ) {
                    id
                    name
                    species_count: pokemon_v2_pokemonspecies_aggregate {
                        aggregate {
                            count
                        }
                    }
                }
            }
        """
        )

        variables = {"habitatName": habitat_name}

        try:
            result = await self.gql_client.execute_async(query, variables)
            return APIResponse(
                data=result, success=True, status_code=200, response_time_ms=0
            )
        except Exception as e:
            return APIResponse(
                success=False, status_code=500, response_time_ms=0, errors=[str(e)]
            )

    async def get_evolution_chains(self, limit: int = 50) -> APIResponse:
        """
        Get evolution chains for progression pattern analysis
        """
        query = gql(
            """
            query GetEvolutionChains($limit: Int!) {
                evolution_chains: pokemon_v2_evolutionchain(limit: $limit) {
                    id
                    species: pokemon_v2_pokemonspecies {
                        id
                        name
                        evolution_order: order
                        evolves_from_species_id
                        pokemon: pokemon_v2_pokemons {
                            id
                            name
                            types: pokemon_v2_pokemontypes {
                                type: pokemon_v2_type {
                                    name
                                }
                            }
                        }
                    }
                }
            }
        """
        )

        variables = {"limit": limit}

        try:
            result = await self.gql_client.execute_async(query, variables)
            return APIResponse(
                data=result, success=True, status_code=200, response_time_ms=0
            )
        except Exception as e:
            return APIResponse(
                success=False, status_code=500, response_time_ms=0, errors=[str(e)]
            )

    async def get_pokemon_species_by_generation(
        self, generation_name: str = "generation-iii", limit: int = 100
    ) -> APIResponse:
        """
        Get Pokemon species by generation (based on working Postman query)
        """
        query = gql(
            """
            query GetPokemonSpeciesByGeneration($generationName: String!, $limit: Int!) {
                gen_species: pokemonspecies(
                    where: {generation: {name: {_eq: $generationName}}}
                    order_by: {id: asc}
                    limit: $limit
                ) {
                    name
                    id
                    generation_id
                    evolution_chain_id
                }
                generation_info: generation(where: {name: {_eq: $generationName}}) {
                    name
                    id
                    pokemon_species: pokemonspecies_aggregate {
                        aggregate {
                            count
                        }
                    }
                }
            }
        """
        )

        variables = {"generationName": generation_name, "limit": limit}

        try:
            result = await self.gql_client.execute_async(query, variables)
            return APIResponse(
                data=result,
                success=True,
                status_code=200,
                response_time_ms=0,
                metadata={
                    "generation": generation_name,
                    "returned_count": len(result.get("gen_species", [])),
                    "total_in_generation": (
                        result.get("generation_info", [{}])[0]
                        .get("pokemon_species", {})
                        .get("aggregate", {})
                        .get("count", 0)
                        if result.get("generation_info")
                        else 0
                    ),
                },
            )
        except Exception as e:
            return APIResponse(
                success=False, status_code=500, response_time_ms=0, errors=[str(e)]
            )
