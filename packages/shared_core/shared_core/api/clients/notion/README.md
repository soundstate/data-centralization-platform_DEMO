# Notion API Client

This package contains a client for interacting with the [Notion](https://www.notion.so/) API. It provides asynchronous HTTP methods to access databases, pages, blocks, and user information with comprehensive error handling and logging.

## Features

- Asynchronous support using `asyncio`
- Rate limiting compliance with Notion API guidelines (3 requests per second)
- Comprehensive database, page, block, and user methods
- Search functionality across pages and databases
- Bearer token authentication
- Correlation-ready data extraction for cross-domain analysis

## Requirements

- Python 3.7+
- `httpx`, `asyncio-throttle`, `tenacity`, `pydantic`
- Valid Notion integration token (free registration required)

## Installation

Include the `shared_core` package in your Python path and install dependencies:

```bash
pip install -e /path/to/shared_core
pip install -r /path/to/services/data_collection/notion_collector/requirements.txt
```

## Configuration

### Environment Variables

Make sure to set the following environment variables:

- `NOTION_INTEGRATION_TOKEN`: Required. Your Notion integration token
- `NOTION_VERSION`: Optional. API version (default: `2022-06-28`)

### Example Usage

```python
import asyncio
from shared_core.config.notion_config import NotionConfig
from shared_core.api.clients.notion import NotionClient

async def run():
    # Initialize client
    config = NotionConfig.get_client_config()
    client = NotionClient(**config)
    
    # Example: Get a database
    response = await client.get_database(database_id="your_database_id")
    if response.success:
        database = response.data
        print(f"Database: {database['title'][0]['text']['content']}")

asyncio.run(run())
```

## API Methods

### Database Methods

#### `get_database`
Retrieve a database by its ID.

```python
await client.get_database(database_id="your_database_id")
```

#### `query_database`
Query a database with optional filtering and sorting.

```python
await client.query_database(database_id="your_database_id", filter_data=filter_obj, sorts=sort_obj)
```

#### `create_database`
Create a new database.

```python
await client.create_database(parent=parent_obj, title=title_obj, properties=properties_obj)
```

#### `update_database`
Update an existing database.

```python
await client.update_database(database_id="your_database_id", title=title_obj)
```

### Page Methods

#### `get_page`
Retrieve a page by its ID.

```python
await client.get_page(page_id="your_page_id")
```

#### `create_page`
Create a new page.

```python
await client.create_page(parent=parent_obj, properties=properties_obj)
```

#### `update_page`
Update an existing page.

```python
await client.update_page(page_id="your_page_id", properties=properties_obj)
```

### Block Methods

#### `get_block`
Retrieve a block by its ID.

```python
await client.get_block(block_id="your_block_id")
```

#### `get_block_children`
Retrieve children of a block.

```python
await client.get_block_children(block_id="your_block_id")
```

#### `append_block_children`
Append child blocks to a parent block.

```python
await client.append_block_children(block_id="your_block_id", children=children_obj)
```

#### `update_block`
Update a block.

```python
await client.update_block(block_id="your_block_id", block_data=block_data_obj)
```

#### `delete_block`
Delete a block.

```python
await client.delete_block(block_id="your_block_id")
```

### User Methods

#### `get_users`
List all users in the workspace.

```python
await client.get_users()
```

#### `get_user`
Retrieve a user by their ID.

```python
await client.get_user(user_id="your_user_id")
```

#### `get_bot_user`
Retrieve the bot user associated with the integration.

```python
await client.get_bot_user()
```

### Search Methods

#### `search`
Search for pages and databases.

```python
await client.search(query="your query", filter_data=filter_obj, sort=sort_obj)
```

### Utility Methods

#### `extract_text_from_rich_text`
Extract plain text from Notion rich text.

```python
text = client.extract_text_from_rich_text(rich_text_obj)
```

#### `extract_correlation_features`
Extract correlation-ready features from Notion data.

```python
features = client.extract_correlation_features(page_data)
```

## Error Handling

Errors are logged via the centralized logging system (`CentralizedLogger`). The client retries failed requests using exponential backoff, as configured.

## Rate Limiting

The client respects Notion's rate limits of 3 requests per second. Exceeding this limit will result in API errors.

## Debug Mode

Enable debug logging by setting `NOTION_DEBUG_MODE=true`. This logs detailed information about all requests.

## Authentication

The client uses Bearer token authentication with your Notion integration token.

## Data Structure

All API responses are wrapped in `APIResponse` objects with the following structure:

```python
class APIResponse:
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    status_code: Optional[int]
```

## Conclusion

This client provides a comprehensive way to interact with the Notion API, allowing you to integrate rich workspace data seamlessly into your applications.
