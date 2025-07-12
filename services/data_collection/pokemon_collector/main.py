"""
Pokemon Data Collection Service

Collects Pokemon data optimized for cross-domain correlations
"""

import asyncio

from shared_core.api.clients.pokemon import PokemonGraphQLClient
from shared_core.utils.centralized_logging import CentralizedLogger

logger = CentralizedLogger.get_logger("pokemon_collector")


class PokemonCollector:
    def __init__(self):
        self.client = PokemonGraphQLClient(debug_mode=True)
        self.batch_size = 100

    async def collect_all_pokemon(self):
        """Collect all Pokemon data for correlation analysis"""
        logger.info("🎮 Starting Pokemon data collection")

        offset = 0
        total_collected = 0

        while True:
            # Fetch batch
            response = await self.client.get_pokemon_for_correlation(
                limit=self.batch_size, offset=offset
            )

            if not response.success:
                logger.error(f"Failed to fetch Pokemon data: {response.errors}")
                break

            pokemon_data = response.data.get("pokemon", [])
            if not pokemon_data:
                break

            # Store raw data
            await self.store_raw_data(pokemon_data)

            # Process for correlations
            await self.process_correlation_data(pokemon_data)

            total_collected += len(pokemon_data)
            offset += self.batch_size

            logger.info(f"Collected {total_collected} Pokemon so far...")

            # Be nice to the API
            await asyncio.sleep(1)

        logger.info(f"✅ Collection complete! Total Pokemon: {total_collected}")

    async def collect_weather_correlation_data(self):
        """Collect specific Pokemon types for weather correlations"""
        weather_types = ["electric", "water", "ice", "fire", "flying"]

        for poke_type in weather_types:
            logger.info(
                f"🌦️ Collecting {poke_type} type Pokemon for weather correlation"
            )
            response = await self.client.get_pokemon_by_type(poke_type)

            if response.success:
                await self.store_correlation_ready_data(
                    data=response.data,
                    correlation_type="weather",
                    metadata={"pokemon_type": poke_type},
                )

    async def collect_habitat_data(self):
        """Collect Pokemon by habitat for geographic correlations"""
        habitats = ["mountain", "cave", "forest", "sea", "urban"]

        for habitat in habitats:
            logger.info(f"🗺️ Collecting {habitat} habitat Pokemon")
            response = await self.client.get_pokemon_by_habitat(habitat)

            if response.success:
                await self.store_correlation_ready_data(
                    data=response.data,
                    correlation_type="geographic",
                    metadata={"habitat": habitat},
                )


if __name__ == "__main__":
    collector = PokemonCollector()

    # Run collection tasks
    asyncio.run(collector.collect_all_pokemon())
    asyncio.run(collector.collect_weather_correlation_data())
    asyncio.run(collector.collect_habitat_data())
