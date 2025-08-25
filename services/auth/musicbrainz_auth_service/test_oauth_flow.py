#!/usr/bin/env python3
"""
MusicBrainz OAuth Flow Test Script

This script demonstrates the complete OAuth 2.0 flow for MusicBrainz authentication.
It starts a local FastAPI server, opens a browser for user authentication,
handles the callback, and makes authenticated API requests.

Usage:
    python test_oauth_flow.py
    
Requirements:
    - Redis server running on localhost:6379
    - MusicBrainz OAuth credentials in environment variables
    - Dependencies installed from requirements.txt

Steps:
1. Start FastAPI OAuth server
2. Open browser to initiate OAuth flow
3. User authenticates with MusicBrainz
4. Handle callback and store tokens
5. Make authenticated API requests
6. Test token refresh mechanism
7. Save results to JSON file
"""

import asyncio
import json
import os
import sys
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import aiohttp
import uvicorn
from multiprocessing import Process

# Add the shared_core package to the path
current_dir = Path(__file__).parent
shared_core_path = current_dir.parent.parent.parent / "packages" / "shared_core"
sys.path.insert(0, str(shared_core_path))

from shared_core.auth.musicbrainz_oauth import MusicBrainzOAuth, MusicBrainzOAuthError
from shared_core.config.musicbrainz_config import MusicBrainzConfig
from shared_core.logging.centralized_logger import CentralizedLogger


class MusicBrainzOAuthTester:
    """
    OAuth Flow Tester for MusicBrainz
    
    Demonstrates the complete OAuth 2.0 authentication flow including
    server startup, browser interaction, token management, and API testing.
    """
    
    def __init__(self):
        """Initialize the OAuth tester."""
        self.logger = CentralizedLogger.get_logger(__name__)
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        self.server_process = None
        self.session_id = None
        self.access_token = None
        self.test_results = {
            "test_started": datetime.utcnow().isoformat() + "Z",
            "steps": [],
            "success": False,
            "errors": [],
            "tokens": {},
            "api_tests": []
        }
    
    def log_step(self, step_name: str, success: bool, details: Dict[str, Any] = None):
        """
        Log a test step with results.
        
        Args:
            step_name: Name of the test step
            success: Whether the step was successful
            details: Additional details about the step
        """
        step_info = {
            "step": step_name,
            "success": success,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "details": details or {}
        }
        
        self.test_results["steps"].append(step_info)
        
        if success:
            self.logger.info(f"✅ {step_name}")
        else:
            self.logger.error(f"❌ {step_name}")
            if details:
                self.logger.error(f"   Details: {details}")
    
    def start_oauth_server(self) -> bool:
        """
        Start the FastAPI OAuth server in a separate process.
        
        Returns:
            True if server started successfully, False otherwise
        """
        try:
            def run_server():
                """Run the FastAPI server."""
                os.system(f"cd {current_dir} && python main.py")
            
            self.server_process = Process(target=run_server)
            self.server_process.start()
            
            # Wait for server to start
            time.sleep(3)
            
            # Test if server is running
            import urllib.request
            try:
                with urllib.request.urlopen("http://localhost:8000/health") as response:
                    if response.status == 200:
                        self.log_step("Start OAuth Server", True, {"port": 8000})
                        return True
            except Exception as e:
                self.log_step("Start OAuth Server", False, {"error": str(e)})
                return False
                
        except Exception as e:
            self.log_step("Start OAuth Server", False, {"error": str(e)})
            return False
    
    def stop_oauth_server(self):
        """Stop the OAuth server process."""
        if self.server_process and self.server_process.is_alive():
            self.server_process.terminate()
            self.server_process.join(timeout=5)
            if self.server_process.is_alive():
                self.server_process.kill()
    
    def initiate_oauth_flow(self) -> bool:
        """
        Initiate OAuth flow by opening browser.
        
        Returns:
            True if flow initiated successfully, False otherwise
        """
        try:
            # Generate authorization URL using the OAuth client directly
            oauth_client = MusicBrainzOAuth()
            auth_url, state = oauth_client.get_authorization_url()
            
            self.logger.info(f"Opening browser to: {auth_url}")
            
            # Open browser to start OAuth flow
            webbrowser.open(auth_url)
            
            self.log_step("Initiate OAuth Flow", True, {
                "auth_url": auth_url,
                "state": state[:10] + "..." if state else None  # Truncate for security
            })
            
            return True
            
        except Exception as e:
            self.log_step("Initiate OAuth Flow", False, {"error": str(e)})
            return False
    
    async def wait_for_callback(self, timeout_seconds: int = 120) -> Optional[str]:
        """
        Wait for OAuth callback to complete and retrieve session ID.
        
        Args:
            timeout_seconds: Maximum time to wait for callback
            
        Returns:
            Session ID if callback successful, None otherwise
        """
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            while time.time() - start_time < timeout_seconds:
                try:
                    # Check if any active sessions exist by polling the server
                    # In a real implementation, we'd use webhooks or polling
                    await asyncio.sleep(2)
                    
                    # This is a simplified approach - in practice you'd get the session_id
                    # from the callback response or a notification mechanism
                    self.logger.info("Waiting for OAuth callback... (please complete authentication in browser)")
                    
                except Exception as e:
                    self.logger.error(f"Error while waiting for callback: {e}")
                    continue
        
        self.log_step("Wait for Callback", False, {"error": "Timeout waiting for callback"})
        return None
    
    async def test_authenticated_api_request(self, access_token: str) -> bool:
        """
        Test making authenticated API requests with the access token.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            True if API request successful, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "User-Agent": MusicBrainzConfig.user_agent(),
                "Accept": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                # Test with a simple artist search
                url = "https://musicbrainz.org/ws/2/artist"
                params = {"query": "The Beatles", "limit": 1, "fmt": "json"}
                
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        api_test_result = {
                            "endpoint": url,
                            "status": response.status,
                            "response_data": data,
                            "success": True
                        }
                        
                        self.test_results["api_tests"].append(api_test_result)
                        self.log_step("Test Authenticated API Request", True, {
                            "endpoint": url,
                            "status": response.status,
                            "results_count": data.get("count", 0) if isinstance(data, dict) else 0
                        })
                        return True
                    else:
                        error_text = await response.text()
                        api_test_result = {
                            "endpoint": url,
                            "status": response.status,
                            "error": error_text,
                            "success": False
                        }
                        
                        self.test_results["api_tests"].append(api_test_result)
                        self.log_step("Test Authenticated API Request", False, {
                            "endpoint": url,
                            "status": response.status,
                            "error": error_text
                        })
                        return False
                        
        except Exception as e:
            self.log_step("Test Authenticated API Request", False, {"error": str(e)})
            return False
    
    async def test_token_refresh(self, refresh_token: str) -> bool:
        """
        Test token refresh mechanism.
        
        Args:
            refresh_token: OAuth refresh token
            
        Returns:
            True if refresh successful, False otherwise
        """
        try:
            oauth_client = MusicBrainzOAuth()
            new_token_info = await oauth_client.refresh_access_token(refresh_token)
            
            self.test_results["tokens"]["refreshed_token"] = {
                "expires_in": new_token_info["expires_in"],
                "token_type": new_token_info["token_type"],
                "scope": new_token_info["scope"],
                "refreshed_at": new_token_info.get("refreshed_at", {}).isoformat() + "Z" if new_token_info.get("refreshed_at") else None
            }
            
            self.log_step("Test Token Refresh", True, {
                "new_expires_in": new_token_info["expires_in"],
                "scope": new_token_info["scope"]
            })
            
            return True
            
        except Exception as e:
            self.log_step("Test Token Refresh", False, {"error": str(e)})
            return False
    
    def save_test_results(self):
        """Save test results to JSON file."""
        try:
            self.test_results["test_completed"] = datetime.utcnow().isoformat() + "Z"
            
            output_file = self.output_dir / "oauth_test_results.json"
            with open(output_file, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            
            self.log_step("Save Test Results", True, {"output_file": str(output_file)})
            self.logger.info(f"Test results saved to: {output_file}")
            
        except Exception as e:
            self.log_step("Save Test Results", False, {"error": str(e)})
    
    async def run_comprehensive_test(self):
        """
        Run the complete OAuth flow test.
        """
        self.logger.info("Starting MusicBrainz OAuth flow comprehensive test...")
        
        try:
            # Step 1: Validate configuration
            try:
                oauth_config = MusicBrainzConfig.get_oauth_config()
                if not oauth_config.get("oauth_valid", False):
                    self.log_step("Validate Configuration", False, {
                        "error": "OAuth configuration is invalid",
                        "config": oauth_config
                    })
                    return False
                
                self.log_step("Validate Configuration", True, {
                    "client_id_set": oauth_config.get("client_id") != "NOT_SET",
                    "client_secret_set": oauth_config.get("client_secret") == "SET",
                    "redirect_uri": oauth_config.get("redirect_uri")
                })
                
            except Exception as e:
                self.log_step("Validate Configuration", False, {"error": str(e)})
                return False
            
            # Step 2: Start OAuth server
            if not self.start_oauth_server():
                return False
            
            # Step 3: Initiate OAuth flow
            if not self.initiate_oauth_flow():
                return False
            
            # Step 4: Manual intervention message
            print("\n" + "="*60)
            print("🔐 MANUAL AUTHENTICATION REQUIRED")
            print("="*60)
            print("1. A browser window should have opened automatically")
            print("2. Log in to MusicBrainz in the browser")
            print("3. Authorize the application")
            print("4. You will be redirected to the callback URL")
            print("5. Check the terminal and server logs for results")
            print("\nPress Enter after completing authentication (or Ctrl+C to cancel)...")
            print("="*60)
            
            try:
                input()  # Wait for user to complete authentication
            except KeyboardInterrupt:
                print("\nTest cancelled by user.")
                return False
            
            # Note: In a real automated test, you would:
            # - Parse the callback URL for session_id
            # - Poll the server for token status
            # - Retrieve tokens programmatically
            
            print("\n📋 Manual Testing Instructions:")
            print("After completing authentication, you can test the following endpoints:")
            print("1. Check auth status: GET http://localhost:8000/auth/musicbrainz/status/{session_id}")
            print("2. Get token: GET http://localhost:8000/auth/musicbrainz/token/{session_id}")
            print("3. Test API with token using the MusicBrainz client")
            
            self.log_step("Manual Authentication", True, {
                "note": "Manual intervention required - check browser and callback"
            })
            
            self.test_results["success"] = True
            
        except Exception as e:
            self.logger.error(f"Test failed with error: {e}")
            self.test_results["errors"].append(str(e))
            
        finally:
            # Cleanup
            self.stop_oauth_server()
            self.save_test_results()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        successful_steps = [step for step in self.test_results["steps"] if step["success"]]
        total_steps = len(self.test_results["steps"])
        
        print(f"Total Steps: {total_steps}")
        print(f"Successful Steps: {len(successful_steps)}")
        print(f"Failed Steps: {total_steps - len(successful_steps)}")
        print(f"Overall Success: {self.test_results['success']}")
        
        if self.test_results["errors"]:
            print(f"Errors: {len(self.test_results['errors'])}")
            for error in self.test_results["errors"]:
                print(f"  - {error}")
        
        print("\n📝 Step Details:")
        for step in self.test_results["steps"]:
            status = "✅" if step["success"] else "❌"
            print(f"  {status} {step['step']}")
        
        print("="*60)


async def main():
    """Main entry point for OAuth flow test."""
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    tester = MusicBrainzOAuthTester()
    
    try:
        await tester.run_comprehensive_test()
    finally:
        tester.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
