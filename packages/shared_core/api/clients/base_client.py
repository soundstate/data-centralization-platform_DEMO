"""
Enhanced Base API Client

Provides comprehensive foundation for all API clients with:
- Built-in debugging and logging
- Rate limiting and retry logic
- Response caching
- Request/response auditing
- Statistical tracking
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import BaseModel, Field

from ...config.logging_config import get_logger


class RequestMetrics(BaseModel):
    """Tracks request performance and statistics"""
    endpoint: str
    method: str
    response_time_ms: float
    status_code: int
    success: bool
    timestamp: datetime
    retry_count: int = 0
    cached: bool = False


class APIResponse(BaseModel):
    """Standardized API response wrapper"""
    data: Optional[Dict[str, Any]] = None
    success: bool
    status_code: int
    response_time_ms: float
    cached: bool = False
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAPIClient:
    """
    Enhanced base API client with comprehensive debugging and reliability features
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        auth_type: str = "Bearer",
        debug_mode: bool = True,
        rate_limit_per_minute: int = 60,
        max_retries: int = 3,
        timeout: int = 30,
        cache_ttl: int = 300,  # 5 minutes
        client_name: str = "base_client"
    ):
        """
        Initialize the enhanced API client
        
        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
            auth_type: Authentication type (Bearer, Basic, etc.)
            debug_mode: Enable detailed logging and debugging
            rate_limit_per_minute: Maximum requests per minute
            max_retries: Maximum retry attempts
            timeout: Request timeout in seconds
            cache_ttl: Cache time-to-live in seconds
            client_name: Client name for logging
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.auth_type = auth_type
        self.debug_mode = debug_mode
        self.rate_limit_per_minute = rate_limit_per_minute
        self.max_retries = max_retries
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        self.client_name = client_name
        
        # Initialize logger
        self.logger = get_logger(f"api_client.{client_name}")
        
        # Request tracking
        self.request_history: List[RequestMetrics] = []
        self.rate_limit_window = timedelta(minutes=1)
        self.last_request_time = datetime.now()
        
        # Response cache
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        
        # HTTP client
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers=self._get_default_headers()
        )
        
        if self.debug_mode:
            self.logger.info(f"Initialized {client_name} client with debug mode enabled")
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for requests"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"DataCentralization/{self.client_name}",
        }
        
        if self.api_key:
            if self.auth_type == "Bearer":
                headers["Authorization"] = f"Bearer {self.api_key}"
            elif self.auth_type == "Basic":
                headers["Authorization"] = f"Basic {self.api_key}"
            elif self.auth_type == "ApiKey":
                headers["X-API-Key"] = self.api_key
        
        return headers
    
    def _get_cache_key(self, method: str, endpoint: str, params: Optional[Dict] = None) -> str:
        """Generate cache key for request"""
        cache_data = {
            "method": method,
            "endpoint": endpoint,
            "params": params or {}
        }
        return f"{self.client_name}:{hash(json.dumps(cache_data, sort_keys=True))}"
    
    def _is_cached_response_valid(self, cached_item: Dict[str, Any]) -> bool:
        """Check if cached response is still valid"""
        if not cached_item:
            return False
        
        cached_time = datetime.fromisoformat(cached_item["timestamp"])
        return datetime.now() - cached_time < timedelta(seconds=self.cache_ttl)
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting"""
        now = datetime.now()
        window_start = now - self.rate_limit_window
        
        # Count requests in the current window
        recent_requests = [
            r for r in self.request_history 
            if r.timestamp > window_start
        ]
        
        if len(recent_requests) >= self.rate_limit_per_minute:
            sleep_time = (self.rate_limit_window.total_seconds() - 
                         (now - recent_requests[0].timestamp).total_seconds()) + 1
            
            if self.debug_mode:
                self.logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
            
            time.sleep(sleep_time)
    
    def _log_request_debug(self, method: str, url: str, **kwargs) -> None:
        """Log request details in debug mode"""
        if not self.debug_mode:
            return
        
        self.logger.debug(f"📡 {method.upper()} {url}")
        
        if kwargs.get("params"):
            self.logger.debug(f"   Params: {kwargs['params']}")
        
        if kwargs.get("json"):
            self.logger.debug(f"   Body: {json.dumps(kwargs['json'], indent=2)}")
        
        if kwargs.get("headers"):
            # Sanitize headers for logging
            safe_headers = {k: v for k, v in kwargs['headers'].items() 
                          if k.lower() not in ['authorization', 'x-api-key']}
            self.logger.debug(f"   Headers: {safe_headers}")
    
    def _log_response_debug(self, response: httpx.Response, response_time_ms: float) -> None:
        """Log response details in debug mode"""
        if not self.debug_mode:
            return
        
        status_emoji = "✅" if response.is_success else "❌"
        self.logger.debug(f"{status_emoji} {response.status_code} ({response_time_ms:.2f}ms)")
        
        if response.headers.get("x-ratelimit-remaining"):
            self.logger.debug(f"   Rate limit remaining: {response.headers['x-ratelimit-remaining']}")
        
        if not response.is_success:
            self.logger.debug(f"   Error: {response.text}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: None
    )
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with retry logic"""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        
        # Apply rate limiting
        self._check_rate_limit()
        
        # Log request details
        self._log_request_debug(method, url, **kwargs)
        
        # Make request
        start_time = time.time()
        response = await self.client.request(method, url, **kwargs)
        response_time_ms = (time.time() - start_time) * 1000
        
        # Log response details
        self._log_response_debug(response, response_time_ms)
        
        # Track metrics
        metrics = RequestMetrics(
            endpoint=endpoint,
            method=method,
            response_time_ms=response_time_ms,
            status_code=response.status_code,
            success=response.is_success,
            timestamp=datetime.now(),
            retry_count=getattr(response, 'retry_count', 0)
        )
        self.request_history.append(metrics)
        
        return response
    
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
        **kwargs
    ) -> APIResponse:
        """
        Make API request with comprehensive error handling and caching
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            use_cache: Whether to use response caching
            **kwargs: Additional httpx request arguments
            
        Returns:
            APIResponse: Standardized response object
        """
        # Check cache first
        cache_key = self._get_cache_key(method, endpoint, params)
        if use_cache and method.upper() == "GET":
            cached_response = self.response_cache.get(cache_key)
            if cached_response and self._is_cached_response_valid(cached_response):
                if self.debug_mode:
                    self.logger.debug(f"🎯 Cache hit for {endpoint}")
                
                return APIResponse(
                    data=cached_response["data"],
                    success=True,
                    status_code=200,
                    response_time_ms=0,
                    cached=True
                )
        
        try:
            # Prepare request arguments
            request_kwargs = {
                "params": params,
                "headers": self._get_default_headers(),
                **kwargs
            }
            
            if data:
                request_kwargs["json"] = data
            
            # Make request
            response = await self._make_request(method, endpoint, **request_kwargs)
            
            # Parse response
            response_data = None
            errors = []
            
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                if response.text:
                    response_data = {"raw_response": response.text}
            
            # Handle errors
            if not response.is_success:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                errors.append(error_msg)
                
                if self.debug_mode:
                    self.logger.error(f"❌ Request failed: {error_msg}")
            
            # Cache successful GET responses
            if (response.is_success and method.upper() == "GET" and 
                use_cache and response_data):
                self.response_cache[cache_key] = {
                    "data": response_data,
                    "timestamp": datetime.now().isoformat()
                }
            
            return APIResponse(
                data=response_data,
                success=response.is_success,
                status_code=response.status_code,
                response_time_ms=(time.time() * 1000) - response.elapsed.total_seconds() * 1000,
                errors=errors,
                metadata={
                    "endpoint": endpoint,
                    "method": method,
                    "headers": dict(response.headers)
                }
            )
            
        except Exception as e:
            error_msg = f"Request exception: {str(e)}"
            self.logger.error(error_msg)
            
            return APIResponse(
                success=False,
                status_code=500,
                response_time_ms=0,
                errors=[error_msg],
                metadata={"endpoint": endpoint, "method": method}
            )
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary"""
        if not self.request_history:
            return {"total_requests": 0}
        
        successful_requests = [r for r in self.request_history if r.success]
        failed_requests = [r for r in self.request_history if not r.success]
        
        return {
            "total_requests": len(self.request_history),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(self.request_history) * 100,
            "average_response_time_ms": sum(r.response_time_ms for r in self.request_history) / len(self.request_history),
            "cache_hits": len([r for r in self.request_history if r.cached]),
            "endpoints_accessed": list(set(r.endpoint for r in self.request_history))
        }
    
    def clear_cache(self) -> None:
        """Clear response cache"""
        self.response_cache.clear()
        if self.debug_mode:
            self.logger.info("🗑️ Response cache cleared")
    
    async def close(self) -> None:
        """Close the HTTP client"""
        await self.client.aclose()
        if self.debug_mode:
            self.logger.info(f"🔒 {self.client_name} client closed")
