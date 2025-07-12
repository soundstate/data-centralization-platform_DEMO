# JS-Codebase Repository Folder Structure

This document contains the complete folder structure of the js-codebase repository, excluding virtual environments, cache directories, and other generated files.

Last updated: July 9, 2025

## Root Structure

```
demo-codebase/
|-- .vscode/
|-- azure/
|   |-- .vscode/
|   |-- containers/
|   |-- deployments/
|   |-- functions/
|   |-- scripts/
|   +-- shared/
|-- data/
|   |-- correlations/
|   |-- embeddings/
|   |-- insights/
|   |-- knowledge_graphs/
|   |-- llm_training/
|   |-- processed/
|   |-- raw/
|   |-- statistics/
|   +-- visualizations/
|-- development/
|   |-- examples/
|   |   |-- api_usage/
|   |   +-- integration_patterns/
|   |-- testing/
|   |   |-- correlation/
|   |   |-- functional/
|   |   |-- integration/
|   |   |-- jobe_shared_test_package/
|   |   |   +-- jobe_shared_test/
|   |   |       +-- api/
|   |   |           |-- helper/
|   |   |           +-- saas/
|   |   |               +-- monday/
|   |   |                   +-- graphql/
|   |   |                       |-- boards/
|   |   |                       |-- config/
|   |   |                       +-- items/
|   |   |                           +-- gather_specific_item_details/
|   |   |-- llm_eval/
|   |   |-- statistical/
|   |   |-- unit/
|   |   +-- visualization/
|   +-- tools/
|       |-- debug_scripts/
|       +-- postman/
|           |-- archive/
|           +-- collections/
|-- flows/
|   |-- correlation_flow/
|   |-- data_ingestion_flow/
|   |-- insight_generation_flow/
|   |-- notion_sync_flow/
|   +-- processing_flow/
|-- functions/
|   +-- temp/
|       |-- .github/
|       |   +-- workflows/
|       |-- .vscode/
|       |-- app/
|       |   |-- config/
|       |   |-- core/
|       |   |-- logs/
|       |   +-- src/
|       |       |-- api/
|       |       |-- functions/
|       |       +-- utils/
|       |-- config/
|       |-- docker/
|       |-- docs/
|       |-- infrastructure/
|       |   |-- bicep/
|       |   +-- terraform/
|       |-- scripts/
|       +-- tests/
|-- infrastructure/
|   |-- azure/
|   |-- docker/
|   |   |-- databases/
|   |   |-- monitoring/
|   |   +-- services/
|   |-- environments/
|   |   |-- development/
|   |   |   |-- config/
|   |   |   +-- secrets/
|   |   |-- production/
|   |   |   |-- config/
|   |   |   +-- secrets/
|   |   |-- shared/
|   |   |   |-- config/
|   |   |   +-- secrets/
|   |   +-- staging/
|   |       |-- config/
|   |       +-- secrets/
|   |-- github_actions/
|   |-- kubernetes/
|   |-- local/
|   +-- pipeline/
|-- lisp/
|   |-- .vscode/
|   |-- commands/
|   |-- docs/
|   +-- functions/
|-- logs/
|-- packages/
|   |-- shared_core/
|   |   |-- .vscode/
|   |   |-- api/
|   |   |   +-- clients/
|   |   |       |-- notion/
|   |   |       |-- openweathermap/
|   |   |       |-- pokemon/
|   |   |       +-- spotify/
|   |   |-- database/
|   |   |   |-- connection/
|   |   |   |-- migrations/
|   |   |   +-- models/
|   |   |-- knowledge_workflows/
|   |   |   |-- data_fusion/
|   |   |   |-- knowledge_extraction/
|   |   |   +-- training_prep/
|   |   |-- models/
|   |   |-- shared_core/
|   |   |   |-- api/
|   |   |   |   |-- clients/
|   |   |   |   |   |-- github/
|   |   |   |   |   |-- musicbrainz/
|   |   |   |   |   |-- spitify/
|   |   |   |   |   |-- tmdb/
|   |   |   |   |   +-- weather/
|   |   |   |   +-- graphql/
|   |   |   |-- config/
|   |   |   |-- helper/
|   |   |   |-- models/
|   |   |   |-- ui/
|   |   |   +-- utils/
|   |   |-- tests/
|   |   +-- utils/
|   |       |-- embedding/
|   |       |-- geographic/
|   |       |-- statistical/
|   |       +-- temporal/
|   +-- workflows/
|-- resources/
|   |-- docs/
|   |-- examples/
|   |   |-- api_integration/
|   |   |-- data_exploration/
|   |   +-- knowledge_queries/
|   |-- guides/
|   +-- technical/
|-- scripts/
|-- server/
|-- services/
|   |-- api_gateway/
|   |-- data_collection/
|   |   |-- entertainment_collector/
|   |   |-- environmental_collector/
|   |   |-- github_collector/
|   |   |-- music_collector/
|   |   |-- musicbrainz_collector/
|   |   |-- pokemon_collector/
|   |   |-- reference_collector/
|   |   |-- spotify_collector/
|   |   |-- tmdb_collector/
|   |   +-- weather_collector/
|   |-- data_processing/
|   |   |-- causation_evaluator/
|   |   |-- correlation_analyzer/
|   |   |-- embedding_generator/
|   |   |-- entity_linker/
|   |   |-- geographic_enricher/
|   |   |-- knowledge_grapher/
|   |   |-- llm_formatter/
|   |   +-- temporal_aligner/
|   |-- delivery/
|   |   |-- alert_system/
|   |   |-- notion_exporter/
|   |   +-- visualization_service/
|   |-- insights/
|   |   |-- correlation_engine/
|   |   |-- pattern_detector/
|   |   |-- report_generator/
|   |   +-- significance_tester/
|   +-- llm_integration/
|       |-- chat_service/
|       |-- embedding_service/
|       |-- evaluation/
|       |-- retrieval_chain/
|       +-- vector_search/
|-- src/
|-- templates/
|-- training/
|   |-- datasets/
|   |-- model_configs/
|   +-- notebooks/
|-- ui/
|   |-- dashboard/
|   |   |-- components/
|   |   |-- hooks/
|   |   |-- pages/
|   |   +-- services/
|   +-- power_apps/
|       +-- demo_screenshots/
+-- web/
```

## Notes

- This structure excludes virtual environments (''.venv''), cache directories (''__pycache__'', ''.pytest_cache''), and other generated files

```
