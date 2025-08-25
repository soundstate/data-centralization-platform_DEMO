#!/usr/bin/env python3
"""
Spotify API Client - Basic Functional Tests

This script provides basic functional tests for the Spotify API client,
including configuration validation, OAuth flow testing, and API endpoint testing.

Usage:
    python test_spotify_basic.py [test_type]
    
    test_type options:
    - config: Test configuration setup
    - oauth: Test OAuth flow
    - token: Test token exchange (requires auth code)
    - client: Test full client functionality
    - all: Run all tests (default)
"""

import asyncio
import os
import sys
from typing import Optional, Dict, Any

# Add the project root and packages directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
packages_dir = os.path.join(project_root, "packages")
sys.path.insert(0, project_root)
sys.path.insert(0, packages_dir)

try:
    from shared_core.config.spotify_config import SpotifyConfig
    from shared_core.auth.spotify_oauth import SpotifyOAuth, SpotifyOAuthError
    from shared_core.api.clients.spotify.spotify_client import SpotifyClient
    from shared_core.utils.centralized_logging import CentralizedLogger
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Make sure you're running from the correct directory and shared_core is installed")
    sys.exit(1)


class SpotifyBasicTests:
    """Basic functional tests for Spotify API client"""
    
    def __init__(self):
        self.logger = CentralizedLogger.get_logger("spotify_basic_tests")
        self.test_results = {}
    
    def print_header(self, title: str, emoji: str = "🧪"):
        """Print a formatted test section header"""
        print(f"\n{emoji} {title}")
        print("=" * (len(title) + 3))
    
    def print_result(self, test_name: str, success: bool, details: str = ""):
        """Print test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        self.test_results[test_name] = success
    
    def test_configuration(self) -> bool:
        """Test Spotify configuration setup"""
        self.print_header("Configuration Tests", "⚙️")
        
        try:
            # Test basic config initialization
            config = SpotifyConfig()
            self.print_result("Config initialization", True)
            
            # Test config summary
            summary = config.get_config_summary()
            self.print_result("Config summary generation", True)
            
            print("\nConfiguration Summary:")
            for key, value in summary.items():
                print(f"  {key}: {value}")
            
            # Test OAuth config
            oauth_config = config.get_oauth_config()
            oauth_valid = oauth_config.get('oauth_valid', False)
            self.print_result("OAuth configuration", oauth_valid)
            
            if not oauth_valid and 'error' in oauth_config:
                print(f"    Error: {oauth_config['error']}")
            
            # Test credential validation
            creds_valid = config.validate_credentials()
            self.print_result("Credential validation", creds_valid)
            
            return oauth_valid and creds_valid
            
        except Exception as e:
            self.print_result("Configuration test", False, f"Exception: {e}")
            return False
    
    async def test_oauth_flow(self) -> Optional[str]:
        """Test OAuth flow and return state parameter"""
        self.print_header("OAuth Flow Tests", "🔐")
        
        try:
            async with SpotifyOAuth() as oauth_client:
                # Test authorization URL generation
                auth_url, state = oauth_client.get_authorization_url()
                self.print_result("Authorization URL generation", True)
                
                print(f"\n🔗 Authorization URL:")
                print(f"{auth_url}")
                print(f"\n🔑 State parameter: {state}")
                
                print(f"\n📋 To continue testing:")
                print("1. Copy the authorization URL above")
                print("2. Paste it in your browser")
                print("3. Log in to Spotify and authorize the app")
                print("4. Copy the 'code' parameter from the callback URL")
                print("5. Run: python test_spotify_basic.py token")
                
                return state
                
        except Exception as e:
            self.print_result("OAuth flow test", False, f"Exception: {e}")
            return None
    
    async def test_token_exchange(self) -> Optional[Dict[str, Any]]:
        """Test token exchange with user-provided authorization code"""
        self.print_header("Token Exchange Tests", "🎟️")
        
        # Get authorization code from user
        auth_code = input("\nEnter the authorization code from callback URL: ").strip()
        if not auth_code:
            self.print_result("Token exchange", False, "Authorization code required")
            return None
        
        state = input("Enter the state parameter (optional): ").strip() or None
        
        try:
            async with SpotifyOAuth() as oauth_client:
                # Exchange code for tokens
                token_info = await oauth_client.exchange_code_for_token(
                    authorization_code=auth_code,
                    state=state or "test-state"  # Use dummy state if not provided
                )
                
                self.print_result("Token exchange", True)
                
                print(f"\n🎫 Token Information:")
                print(f"Access token: {token_info['access_token'][:20]}...")
                refresh_token = token_info.get('refresh_token')
                if refresh_token:
                    print(f"Refresh token: {refresh_token[:20]}...")
                else:
                    print("Refresh token: Not provided")
                print(f"Expires at: {token_info['expires_at']}")
                print(f"Scopes: {token_info.get('scope', 'N/A')}")
                
                # Test token validation
                is_valid = await oauth_client.validate_token(token_info['access_token'])
                self.print_result("Token validation", is_valid)
                
                # Test token expiration check
                is_expired = oauth_client.is_token_expired(token_info)
                self.print_result("Token expiration check", not is_expired, 
                                f"Token expired: {is_expired}")
                
                return token_info
                
        except SpotifyOAuthError as e:
            self.print_result("Token exchange", False, f"OAuth error: {e}")
            return None
        except Exception as e:
            self.print_result("Token exchange", False, f"Exception: {e}")
            return None
    
    async def test_client_functionality(self) -> bool:
        """Test full Spotify client functionality with authentication"""
        self.print_header("Client Functionality Tests", "🎵")
        
        try:
            # Initialize client using config
            client_id = SpotifyConfig.client_id()
            client_secret = SpotifyConfig.client_secret()
            redirect_uri = SpotifyConfig.redirect_uri()
            
            async with SpotifyClient(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                debug_mode=True
            ) as client:
                
                # Test OAuth URL generation
                auth_url, state = await client.get_oauth_authorization_url()
                self.print_result("Client OAuth URL generation", True)
                
                print(f"\n🔗 Visit this URL to authorize:")
                print(f"{auth_url}")
                
                # Get authorization code from user
                auth_code = input("\nEnter authorization code from callback: ").strip()
                if not auth_code:
                    self.print_result("Client authentication", False, "Authorization code required")
                    return False
                
                # Exchange for tokens
                auth_success = await client.oauth_exchange_code_for_tokens(
                    authorization_code=auth_code,
                    state=state,
                    expected_state=state
                )
                
                self.print_result("Client token exchange", auth_success)
                if not auth_success:
                    return False
                
                print("\n🧪 Testing API endpoints...")
                
                # Test user profile
                profile_response = await client.get_user_profile()
                profile_success = profile_response.success
                self.print_result("Get user profile", profile_success)
                
                if profile_success:
                    user = profile_response.data
                    print(f"    👤 User: {user.get('display_name', 'N/A')} ({user.get('id')})")
                    print(f"    📧 Email: {user.get('email', 'N/A')}")
                    print(f"    🎵 Followers: {user.get('followers', {}).get('total', 0)}")
                
                # Test top tracks
                top_tracks_response = await client.get_user_top_tracks(limit=3)
                top_tracks_success = top_tracks_response.success
                self.print_result("Get top tracks", top_tracks_success)
                
                if top_tracks_success:
                    tracks = top_tracks_response.data.get('items', [])
                    print(f"    🔥 Your Top {len(tracks)} Tracks:")
                    for i, track in enumerate(tracks, 1):
                        artists = ', '.join([a['name'] for a in track.get('artists', [])])
                        print(f"      {i}. {track.get('name')} - {artists}")
                        
                        # Test audio features for first track
                        if i == 1:
                            track_id = track['id']
                            features_response = await client.get_track_audio_features(track_id)
                            features_success = features_response.success
                            self.print_result("Get audio features", features_success)
                            
                            if features_success:
                                features = features_response.data
                                correlation_features = client.extract_audio_features_for_correlation(features)
                                print(f"        🎶 Audio Features: {list(correlation_features.keys())}")
                
                # Test recently played
                recent_response = await client.get_user_recently_played(limit=3)
                recent_success = recent_response.success
                self.print_result("Get recently played", recent_success)
                
                if recent_success:
                    recent_tracks = recent_response.data.get('items', [])
                    print(f"    🕐 Recently Played ({len(recent_tracks)} tracks):")
                    for item in recent_tracks:
                        track = item.get('track', {})
                        played_at = item.get('played_at')
                        artists = ', '.join([a['name'] for a in track.get('artists', [])])
                        print(f"      • {track.get('name')} - {artists}")
                
                # Test token validation methods
                token_valid = await client.validate_access_token()
                self.print_result("Token validation method", token_valid)
                
                token_expired = client.is_token_expired()
                self.print_result("Token expiration check method", not token_expired)
                
                return all([auth_success, profile_success, top_tracks_success, recent_success, token_valid])
                
        except Exception as e:
            self.print_result("Client functionality test", False, f"Exception: {e}")
            return False
    
    async def run_all_tests(self) -> None:
        """Run all available tests"""
        self.print_header("Spotify API Client - Comprehensive Tests", "🎵")
        
        # Test configuration
        config_success = self.test_configuration()
        
        if not config_success:
            print("\n❌ Configuration tests failed. Please check your environment setup.")
            return
        
        # Test OAuth flow
        state = await self.test_oauth_flow()
        if not state:
            print("\n❌ OAuth flow tests failed.")
            return
        
        print(f"\n⏸️  Tests paused. Please complete authorization in browser.")
        print(f"   Run 'python {os.path.basename(__file__)} client' when ready to continue.")
    
    def print_summary(self) -> None:
        """Print test results summary"""
        self.print_header("Test Results Summary", "📊")
        
        passed = sum(1 for success in self.test_results.values() if success)
        total = len(self.test_results)
        
        for test_name, success in self.test_results.items():
            status = "✅" if success else "❌"
            print(f"{status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print(f"❌ {total - passed} tests failed")


def main():
    """Main function to handle command line arguments and run tests"""
    
    # Check command line arguments
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if test_type not in ["config", "oauth", "token", "client", "all"]:
        print("Usage: python test_spotify_basic.py [config|oauth|token|client|all]")
        sys.exit(1)
    
    # Create test instance
    tester = SpotifyBasicTests()
    
    try:
        if test_type == "config":
            success = tester.test_configuration()
            tester.print_summary()
            
        elif test_type == "oauth":
            asyncio.run(tester.test_oauth_flow())
            tester.print_summary()
            
        elif test_type == "token":
            asyncio.run(tester.test_token_exchange())
            tester.print_summary()
            
        elif test_type == "client":
            asyncio.run(tester.test_client_functionality())
            tester.print_summary()
            
        elif test_type == "all":
            asyncio.run(tester.run_all_tests())
            tester.print_summary()
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
