"""
Pokemon GraphQL Query Library

Pre-built queries for common correlation analysis patterns
"""

# Weather correlation queries
WEATHER_TYPE_CORRELATIONS = {
    "electric": """
        query ElectricPokemonForWeather {
            pokemon: pokemon_v2_pokemontype(
                where: {pokemon_v2_type: {name: {_eq: "electric"}}}
                limit: 500
            ) {
                pokemon: pokemon_v2_pokemon {
                    id
                    name
                    species: pokemon_v2_pokemonspecy {
                        generation_id
                        habitat: pokemon_v2_pokemonhabitat { name }
                        color: pokemon_v2_pokemoncolor { name }
                    }
                }
            }
        }
    """,
    "water": """
        query WaterPokemonForWeather {
            pokemon: pokemon_v2_pokemontype(
                where: {pokemon_v2_type: {name: {_eq: "water"}}}
                limit: 500
            ) {
                pokemon: pokemon_v2_pokemon {
                    id
                    name
                    species: pokemon_v2_pokemonspecy {
                        generation_id
                        habitat: pokemon_v2_pokemonhabitat { name }
                    }
                }
            }
        }
    """,
    "ice": """
        query IcePokemonForWeather {
            pokemon: pokemon_v2_pokemontype(
                where: {pokemon_v2_type: {name: {_eq: "ice"}}}
                limit: 500
            ) {
                pokemon: pokemon_v2_pokemon {
                    id
                    name
                    species: pokemon_v2_pokemonspecy {
                        generation_id
                        habitat: pokemon_v2_pokemonhabitat { name }
                    }
                }
            }
        }
    """,
}

# Geographic correlation queries
HABITAT_QUERIES = {
    "mountain": "mountain",
    "cave": "cave",
    "forest": "forest",
    "grassland": "grassland",
    "sea": "sea",
    "urban": "urban",
    "waters-edge": "waters-edge",
}

# Temporal correlation query
GENERATION_TIMELINE_QUERY = """
    query PokemonGenerationTimeline {
        generations: pokemon_v2_generation(order_by: {id: asc}) {
            id
            name
            main_region: pokemon_v2_region { name }
            version_groups: pokemon_v2_versiongroups {
                versions: pokemon_v2_versions {
                    name
                    release_date
                }
            }
            species_count: pokemon_v2_pokemonspecies_aggregate {
                aggregate { count }
            }
            types_introduced: pokemon_v2_types(
                where: {generation_id: {_eq: id}}
            ) {
                name
            }
        }
    }
"""
