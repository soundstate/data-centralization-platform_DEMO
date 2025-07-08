# JS-Codebase Repository Folder Structure

This document contains the complete folder structure of the js-codebase repository, excluding virtual environments, cache directories, and other generated files.

Last updated: July 8, 2025

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
|   |-- knowledge_graphs/
|   |-- llm_training/
|   |-- processed/
|   +-- raw/
|-- development/
|   |-- examples/
|   |   |-- api_usage/
|   |   +-- integration_patterns/
|   |-- testing/
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
|   |   +-- unit/
|   +-- tools/
|       |-- debug_scripts/
|       +-- postman/
|           |-- archive/
|           +-- collections/
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
|-- logs/
|-- packages/
|   |-- shared_core/
|   |   |-- .vscode/
|   |   |-- knowledge_workflows/
|   |   |   |-- data_fusion/
|   |   |   |-- knowledge_extraction/
|   |   |   +-- training_prep/
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
|   |   |   |-- models/
|   |   |   |-- ui/
|   |   |   +-- utils/
|   |   +-- tests/
|   +-- workflows/
|-- resources/
|   |-- docs/
|   +-- examples/
|       |-- api_integration/
|       |-- data_exploration/
|       +-- knowledge_queries/
|-- scripts/
|-- server/
|-- services/
|   |-- api_gateway/
|   |-- data_collection/
|   |   |-- entertainment_collector/
|   |   |-- environmental_collector/
|   |   |-- music_collector/
|   |   +-- reference_collector/
|   +-- data_processing/
|       |-- entity_linker/
|       |-- knowledge_grapher/
|       +-- llm_formatter/
|-- src/
|-- templates/
|-- training/
|   |-- datasets/
|   |-- model_configs/
|   +-- notebooks/
|-- ui/
|   |-- dashboard/
|   +-- power_apps/
|       +-- demo_screenshots/
+-- web/
```

## Notes

- This structure excludes virtual environments (''.venv''), cache directories (''**pycache**'', ''.pytest_cache''), and other generated files
