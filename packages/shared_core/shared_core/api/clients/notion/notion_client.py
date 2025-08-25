"""
Notion API Client

This module provides a client for interacting with the Notion API.
It follows the established patterns for API clients in the shared_core package.

The Notion API provides access to:
- Database operations (query, create, update)
- Page operations (retrieve, create, update)
- Block operations (retrieve, create, update, delete)
- User information
- Search functionality

Features:
- Rate limiting compliance with Notion API guidelines
- Retry logic with exponential backoff
- Comprehensive error handling
- Correlation-ready data extraction
- Temporal and categorical context
- Rich text and property handling
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin

from ....config.base_client import APIResponse, BaseAPIClient
from ....utils.centralized_logging import CentralizedLogger


class NotionClient(BaseAPIClient):
    """
    Notion API Client for accessing the Notion API.
    
    This client provides comprehensive access to Notion databases, pages, and blocks
    with built-in rate limiting, error handling, and correlation-ready data extraction.
    
    Rate Limits:
    - 3 requests per second average
    - Burst limit handled by API
    
    Authentication:
    - Integration token required
    - Bearer token authentication
    """
    
    def __init__(
        self,
        integration_token: str,
        base_url: str = "https://api.notion.com/v1",
        notion_version: str = "2022-06-28",
        rate_limit_per_second: float = 3.0,
        max_retries: int = 3,
        timeout: int = 30,
        debug_mode: bool = False
    ):
        """
        Initialize Notion API client.
        
        Args:
            integration_token: Notion integration token
            base_url: Base URL for Notion API (default: https://api.notion.com/v1)
            notion_version: Notion API version (default: 2022-06-28)
            rate_limit_per_second: Rate limit in requests per second (default: 3.0)
            max_retries: Maximum number of retry attempts (default: 3)
            timeout: Request timeout in seconds (default: 30)
            debug_mode: Enable debug logging (default: False)
        """
        super().__init__(
            base_url=base_url,
            rate_limit_per_second=rate_limit_per_second,
            max_retries=max_retries,
            timeout=timeout,
            debug_mode=debug_mode
        )
        
        self.integration_token = integration_token
        self.notion_version = notion_version
        self.logger = CentralizedLogger.get_logger(__name__)
        
        # Default headers for all requests
        self.headers = {
            "Authorization": f"Bearer {integration_token}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version
        }
        
        if debug_mode:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Notion client initialized in debug mode")
    
    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Make a request to the Notion API.
        
        Args:
            endpoint: API endpoint (e.g., "/databases")
            method: HTTP method (default: GET)
            params: Query parameters
            data: Request body data
            
        Returns:
            APIResponse object with success status and data
        """
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        try:
            response = await self._request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=self.headers
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                return APIResponse(success=True, data=data, status_code=response.status_code)
            else:
                error_msg = f"Notion API error: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                
                self.logger.error(error_msg)
                return APIResponse(
                    success=False,
                    error=error_msg,
                    status_code=response.status_code
                )
                
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            self.logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    # Database Methods
    async def get_database(self, database_id: str) -> APIResponse:
        """
        Retrieve a database by its ID.
        
        Args:
            database_id: The ID of the database to retrieve
        
        Returns:
            APIResponse with database information
        """
        return await self._make_request(f"/databases/{database_id}")
    
    async def query_database(
        self,
        database_id: str,
        filter_data: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None
    ) -> APIResponse:
        """
        Query a database with optional filtering and sorting.
        
        Args:
            database_id: The ID of the database to query
            filter_data: Filter criteria for the query
            sorts: Sort criteria for the query
            start_cursor: Pagination cursor
            page_size: Number of results per page (max 100)
        
        Returns:
            APIResponse with query results
        """
        data = {}
        
        if filter_data:
            data["filter"] = filter_data
        
        if sorts:
            data["sorts"] = sorts
        
        if start_cursor:
            data["start_cursor"] = start_cursor
        
        if page_size:
            data["page_size"] = min(page_size, 100)
        
        return await self._make_request(
            f"/databases/{database_id}/query",
            method="POST",
            data=data
        )
    
    async def create_database(
        self,
        parent: Dict[str, Any],
        title: List[Dict[str, Any]],
        properties: Dict[str, Any],
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Create a new database.
        
        Args:
            parent: Parent page or workspace
            title: Database title
            properties: Database properties schema
            icon: Database icon (optional)
            cover: Database cover (optional)
        
        Returns:
            APIResponse with created database information
        """
        data = {
            "parent": parent,
            "title": title,
            "properties": properties
        }
        
        if icon:
            data["icon"] = icon
        
        if cover:
            data["cover"] = cover
        
        return await self._make_request("/databases", method="POST", data=data)
    
    async def update_database(
        self,
        database_id: str,
        title: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Update an existing database.
        
        Args:
            database_id: The ID of the database to update
            title: Updated database title
            properties: Updated database properties
            icon: Updated database icon
            cover: Updated database cover
        
        Returns:
            APIResponse with updated database information
        """
        data = {}
        
        if title:
            data["title"] = title
        
        if properties:
            data["properties"] = properties
        
        if icon:
            data["icon"] = icon
        
        if cover:
            data["cover"] = cover
        
        return await self._make_request(
            f"/databases/{database_id}",
            method="PATCH",
            data=data
        )
    
    # Page Methods
    async def get_page(self, page_id: str) -> APIResponse:
        """
        Retrieve a page by its ID.
        
        Args:
            page_id: The ID of the page to retrieve
        
        Returns:
            APIResponse with page information
        """
        return await self._make_request(f"/pages/{page_id}")
    
    async def create_page(
        self,
        parent: Dict[str, Any],
        properties: Dict[str, Any],
        children: Optional[List[Dict[str, Any]]] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Create a new page.
        
        Args:
            parent: Parent database or page
            properties: Page properties
            children: Child blocks (optional)
            icon: Page icon (optional)
            cover: Page cover (optional)
        
        Returns:
            APIResponse with created page information
        """
        data = {
            "parent": parent,
            "properties": properties
        }
        
        if children:
            data["children"] = children
        
        if icon:
            data["icon"] = icon
        
        if cover:
            data["cover"] = cover
        
        return await self._make_request("/pages", method="POST", data=data)
    
    async def update_page(
        self,
        page_id: str,
        properties: Optional[Dict[str, Any]] = None,
        archived: Optional[bool] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Update an existing page.
        
        Args:
            page_id: The ID of the page to update
            properties: Updated page properties
            archived: Archive status
            icon: Updated page icon
            cover: Updated page cover
        
        Returns:
            APIResponse with updated page information
        """
        data = {}
        
        if properties:
            data["properties"] = properties
        
        if archived is not None:
            data["archived"] = archived
        
        if icon:
            data["icon"] = icon
        
        if cover:
            data["cover"] = cover
        
        return await self._make_request(
            f"/pages/{page_id}",
            method="PATCH",
            data=data
        )
    
    # Block Methods
    async def get_block(self, block_id: str) -> APIResponse:
        """
        Retrieve a block by its ID.
        
        Args:
            block_id: The ID of the block to retrieve
        
        Returns:
            APIResponse with block information
        """
        return await self._make_request(f"/blocks/{block_id}")
    
    async def get_block_children(
        self,
        block_id: str,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None
    ) -> APIResponse:
        """
        Retrieve children of a block.
        
        Args:
            block_id: The ID of the parent block
            start_cursor: Pagination cursor
            page_size: Number of results per page (max 100)
        
        Returns:
            APIResponse with child blocks
        """
        params = {}
        
        if start_cursor:
            params["start_cursor"] = start_cursor
        
        if page_size:
            params["page_size"] = min(page_size, 100)
        
        return await self._make_request(
            f"/blocks/{block_id}/children",
            params=params
        )
    
    async def append_block_children(
        self,
        block_id: str,
        children: List[Dict[str, Any]]
    ) -> APIResponse:
        """
        Append child blocks to a parent block.
        
        Args:
            block_id: The ID of the parent block
            children: List of child blocks to append
        
        Returns:
            APIResponse with operation result
        """
        data = {"children": children}
        
        return await self._make_request(
            f"/blocks/{block_id}/children",
            method="PATCH",
            data=data
        )
    
    async def update_block(
        self,
        block_id: str,
        block_data: Dict[str, Any]
    ) -> APIResponse:
        """
        Update a block.
        
        Args:
            block_id: The ID of the block to update
            block_data: Updated block data
        
        Returns:
            APIResponse with updated block information
        """
        return await self._make_request(
            f"/blocks/{block_id}",
            method="PATCH",
            data=block_data
        )
    
    async def delete_block(self, block_id: str) -> APIResponse:
        """
        Delete a block.
        
        Args:
            block_id: The ID of the block to delete
        
        Returns:
            APIResponse with operation result
        """
        return await self._make_request(
            f"/blocks/{block_id}",
            method="DELETE"
        )
    
    # User Methods
    async def get_users(
        self,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None
    ) -> APIResponse:
        """
        List all users in the workspace.
        
        Args:
            start_cursor: Pagination cursor
            page_size: Number of results per page (max 100)
        
        Returns:
            APIResponse with user list
        """
        params = {}
        
        if start_cursor:
            params["start_cursor"] = start_cursor
        
        if page_size:
            params["page_size"] = min(page_size, 100)
        
        return await self._make_request("/users", params=params)
    
    async def get_user(self, user_id: str) -> APIResponse:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve
        
        Returns:
            APIResponse with user information
        """
        return await self._make_request(f"/users/{user_id}")
    
    async def get_bot_user(self) -> APIResponse:
        """
        Retrieve the bot user associated with the integration.
        
        Returns:
            APIResponse with bot user information
        """
        return await self._make_request("/users/me")
    
    # Search Methods
    async def search(
        self,
        query: Optional[str] = None,
        sort: Optional[Dict[str, Any]] = None,
        filter_data: Optional[Dict[str, Any]] = None,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None
    ) -> APIResponse:
        """
        Search for pages and databases.
        
        Args:
            query: Search query
            sort: Sort criteria
            filter_data: Filter criteria
            start_cursor: Pagination cursor
            page_size: Number of results per page (max 100)
        
        Returns:
            APIResponse with search results
        """
        data = {}
        
        if query:
            data["query"] = query
        
        if sort:
            data["sort"] = sort
        
        if filter_data:
            data["filter"] = filter_data
        
        if start_cursor:
            data["start_cursor"] = start_cursor
        
        if page_size:
            data["page_size"] = min(page_size, 100)
        
        return await self._make_request("/search", method="POST", data=data)
    
    # Utility Methods
    def extract_text_from_rich_text(self, rich_text: List[Dict[str, Any]]) -> str:
        """
        Extract plain text from Notion rich text format.
        
        Args:
            rich_text: List of rich text objects
        
        Returns:
            Plain text string
        """
        if not rich_text:
            return ""
        
        return "".join([text_obj.get("plain_text", "") for text_obj in rich_text])
    
    def extract_correlation_features(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract correlation-ready features from Notion page data.
        
        Args:
            page_data: Raw Notion API response data
        
        Returns:
            Dictionary with correlation features
        """
        features = {}
        
        # Basic page information
        if "id" in page_data:
            features["page_id"] = page_data["id"]
        
        if "object" in page_data:
            features["object_type"] = page_data["object"]
        
        if "created_time" in page_data:
            features["created_time"] = page_data["created_time"]
        
        if "last_edited_time" in page_data:
            features["last_edited_time"] = page_data["last_edited_time"]
        
        if "archived" in page_data:
            features["is_archived"] = page_data["archived"]
        
        # Extract properties
        if "properties" in page_data:
            properties = page_data["properties"]
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get("type")
                
                if prop_type == "title":
                    title_text = self.extract_text_from_rich_text(prop_data.get("title", []))
                    features[f"title_{prop_name}"] = title_text
                
                elif prop_type == "rich_text":
                    rich_text = self.extract_text_from_rich_text(prop_data.get("rich_text", []))
                    features[f"text_{prop_name}"] = rich_text
                
                elif prop_type == "number":
                    features[f"number_{prop_name}"] = prop_data.get("number")
                
                elif prop_type == "select":
                    select_value = prop_data.get("select")
                    if select_value:
                        features[f"select_{prop_name}"] = select_value.get("name")
                
                elif prop_type == "multi_select":
                    multi_select = prop_data.get("multi_select", [])
                    features[f"multi_select_{prop_name}"] = [item.get("name") for item in multi_select]
                
                elif prop_type == "date":
                    date_value = prop_data.get("date")
                    if date_value:
                        features[f"date_{prop_name}"] = date_value.get("start")
                
                elif prop_type == "checkbox":
                    features[f"checkbox_{prop_name}"] = prop_data.get("checkbox")
                
                elif prop_type == "url":
                    features[f"url_{prop_name}"] = prop_data.get("url")
                
                elif prop_type == "email":
                    features[f"email_{prop_name}"] = prop_data.get("email")
                
                elif prop_type == "phone_number":
                    features[f"phone_{prop_name}"] = prop_data.get("phone_number")
        
        return features
    
    def extract_temporal_context(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract temporal context from Notion page data.
        
        Args:
            page_data: Raw Notion API response data
        
        Returns:
            Dictionary with temporal context
        """
        context = {
            "collection_timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if "created_time" in page_data:
            context["created_time"] = page_data["created_time"]
        
        if "last_edited_time" in page_data:
            context["last_edited_time"] = page_data["last_edited_time"]
        
        # Extract date properties
        if "properties" in page_data:
            properties = page_data["properties"]
            for prop_name, prop_data in properties.items():
                if prop_data.get("type") == "date":
                    date_value = prop_data.get("date")
                    if date_value:
                        context[f"date_{prop_name}"] = date_value.get("start")
                        if date_value.get("end"):
                            context[f"date_{prop_name}_end"] = date_value.get("end")
        
        return context
    
    def categorize_content(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Categorize Notion content for correlation analysis.
        
        Args:
            page_data: Raw Notion API response data
        
        Returns:
            Dictionary with content categories
        """
        categories = {}
        
        # Object type
        if "object" in page_data:
            categories["object_type"] = page_data["object"]
        
        # Archive status
        if "archived" in page_data:
            categories["is_archived"] = page_data["archived"]
            categories["status"] = "archived" if page_data["archived"] else "active"
        
        # Parent type
        if "parent" in page_data:
            parent_type = page_data["parent"].get("type")
            categories["parent_type"] = parent_type
        
        # Extract categorical properties
        if "properties" in page_data:
            properties = page_data["properties"]
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get("type")
                
                if prop_type == "select":
                    select_value = prop_data.get("select")
                    if select_value:
                        categories[f"select_{prop_name}"] = select_value.get("name")
                
                elif prop_type == "multi_select":
                    multi_select = prop_data.get("multi_select", [])
                    categories[f"multi_select_{prop_name}"] = [item.get("name") for item in multi_select]
                
                elif prop_type == "checkbox":
                    categories[f"checkbox_{prop_name}"] = prop_data.get("checkbox")
        
        return categories
    
    def prepare_correlation_data(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare complete correlation-ready data structure.
        
        Args:
            page_data: Raw Notion API response data
        
        Returns:
            Complete correlation data structure
        """
        return {
            "raw_data": page_data,
            "correlation_features": self.extract_correlation_features(page_data),
            "temporal_context": self.extract_temporal_context(page_data),
            "content_categories": self.categorize_content(page_data),
            "data_source": "notion",
            "api_version": self.notion_version,
            "collection_timestamp": datetime.utcnow().isoformat() + "Z"
        }
