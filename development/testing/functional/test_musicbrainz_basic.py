#!/usr/bin/env python3
"""
Basic MusicBrainz API Functional Test

This script tests the basic functionality of the MusicBrainz API client
without requiring OAuth authentication. Use this to verify your setup
before proceeding with OAuth implementation.

Usage:
    python test_musicbrainz_basic.py
    
Requirements:
    - MUSICBRAINZ_USER_AGENT environment variable set
    - Internet connection
    - shared_core package available in Python path
"""

import asyncio
import os
import sys
from pathlib import Path

# Add shared_core to path
current_dir = Path(__file__).parent
shared_core_path = current_dir.parent.parent.parent / "packages" / "shared_core"
sys.path.insert(0, str(shared_core_path))

async def test_basic_functionality():
    """Test basic MusicBrainz API functionality."""
    
    print("🎵 MusicBrainz API Basic Test")
    print("=" * 50)
    
    try:
        # Test 1: Configuration
        print("📋 Test 1: Configuration Validation")
        from shared_core.config.musicbrainz_config import MusicBrainzConfig
        
        try:
            config_summary = MusicBrainzConfig.get_config_summary()
            print(f"✅ Configuration loaded successfully")
            print(f"   User-Agent: {config_summary.get('user_agent', 'NOT_SET')}")
            print(f"   Rate Limit: {config_summary.get('rate_limit_per_second')} req/sec")
            print(f"   Debug Mode: {config_summary.get('debug_mode')}")
            print(f"   Valid: {config_summary.get('is_valid')}")
            
            if not config_summary.get('is_valid'):
                print("❌ Configuration is invalid. Please check your MUSICBRAINZ_USER_AGENT.")
                return False
                
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            print("💡 Make sure MUSICBRAINZ_USER_AGENT is set in your environment")
            return False
        
        # Test 2: Client Initialization
        print("\n🔧 Test 2: Client Initialization")
        from shared_core.api.clients.musicbrainz import MusicBrainzClient
        
        try:
            client_config = MusicBrainzConfig.get_client_config()
            client = MusicBrainzClient(**client_config)
            print("✅ MusicBrainz client initialized successfully")
        except Exception as e:
            print(f"❌ Client initialization failed: {e}")
            return False
        
        # Test 3: Basic API Request
        print("\n🌐 Test 3: Basic API Request")
        try:
            response = await client.search_artist("The Beatles", limit=1)
            
            if response.success:
                artists = response.data.get("artists", [])
                if artists:
                    artist = artists[0]
                    print("✅ API request successful")
                    print(f"   Found: {artist.get('name')}")
                    print(f"   MBID: {artist.get('id')}")
                    print(f"   Score: {artist.get('score')}")
                    print(f"   Type: {artist.get('type')}")
                else:
                    print("⚠️  API request successful but no results found")
            else:
                print(f"❌ API request failed: {response.error}")
                print(f"   Status Code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API request error: {e}")
            return False
        
        # Test 4: Data Correlation Features
        print("\n🔗 Test 4: Data Correlation Features")
        try:
            if artists:
                correlation_data = client.prepare_correlation_data(artists[0])
                print("✅ Data correlation processing successful")
                print(f"   Data Source: {correlation_data.get('data_source')}")
                print(f"   Has Raw Data: {'raw_data' in correlation_data}")
                print(f"   Has Features: {'correlation_features' in correlation_data}")
                print(f"   Has Temporal Context: {'temporal_context' in correlation_data}")
            
        except Exception as e:
            print(f"❌ Data correlation error: {e}")
            return False
        
        # Test 5: Rate Limiting Test
        print("\n⏱️  Test 5: Rate Limiting Behavior")
        try:
            import time
            
            start_time = time.time()
            
            # Make multiple requests to test rate limiting
            tasks = [
                client.search_artist("Beatles", limit=1),
                client.search_artist("Radiohead", limit=1),
                client.search_artist("Pink Floyd", limit=1)
            ]
            
            results = await asyncio.gather(*tasks)
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            successful_requests = sum(1 for result in results if result.success)
            
            print(f"✅ Rate limiting test completed")
            print(f"   Requests made: {len(tasks)}")
            print(f"   Successful: {successful_requests}")
            print(f"   Time elapsed: {elapsed:.2f} seconds")
            print(f"   Average rate: {len(tasks)/elapsed:.2f} req/sec")
            
            if elapsed >= 2.0:  # Should take at least 2 seconds for 3 requests at 1 req/sec
                print("   ✅ Rate limiting is working correctly")
            else:
                print("   ⚠️  Rate limiting may not be working as expected")
            
        except Exception as e:
            print(f"❌ Rate limiting test error: {e}")
            return False
        
        # Test 6: OAuth Configuration Check (Optional)
        print("\n🔐 Test 6: OAuth Configuration Check")
        try:
            oauth_config = MusicBrainzConfig.get_oauth_config()
            print(f"   Client ID Set: {oauth_config.get('client_id') != 'NOT_SET'}")
            print(f"   Client Secret Set: {oauth_config.get('client_secret') == 'SET'}")
            print(f"   Redirect URI: {oauth_config.get('redirect_uri')}")
            print(f"   OAuth Valid: {oauth_config.get('oauth_valid', False)}")
            
            if oauth_config.get('oauth_valid', False):
                print("✅ OAuth configuration is valid - ready for authenticated requests")
            else:
                print("ℹ️  OAuth not configured - only unauthenticated requests available")
                
        except Exception as e:
            print(f"⚠️  OAuth configuration check failed: {e}")
            print("   This is expected if OAuth credentials are not configured")
        
        # Cleanup
        await client.close()
        
        print("\n" + "=" * 50)
        print("🎉 All basic tests completed successfully!")
        print("\nNext Steps:")
        print("1. ✅ Basic API client is working")
        print("2. 🔐 Set up OAuth for authenticated access (optional)")
        print("3. 🚀 Start collecting MusicBrainz data")
        print("\nTo set up OAuth authentication:")
        print("   - Register at: https://musicbrainz.org/account/applications")
        print("   - Run: cd ../oauth && python test_oauth_flow.py")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_environment():
    """Check if required environment variables are set."""
    
    print("🔍 Environment Check")
    print("-" * 30)
    
    user_agent = os.getenv("MUSICBRAINZ_USER_AGENT")
    if user_agent:
        print(f"✅ MUSICBRAINZ_USER_AGENT: {user_agent}")
    else:
        print("❌ MUSICBRAINZ_USER_AGENT: Not set")
        print("\n💡 To fix this, set your User-Agent:")
        print('export MUSICBRAINZ_USER_AGENT="YourApp/1.0.0 (contact@example.com)"')
        return False
    
    # Check optional OAuth variables
    client_id = os.getenv("MUSICBRAINZ_CLIENT_ID")
    client_secret = os.getenv("MUSICBRAINZ_CLIENT_SECRET")
    
    if client_id and client_secret:
        print(f"✅ MUSICBRAINZ_CLIENT_ID: {client_id[:10]}...")
        print("✅ MUSICBRAINZ_CLIENT_SECRET: Set")
        print("🔐 OAuth credentials configured - full functionality available")
    else:
        print("ℹ️  OAuth credentials not set - basic functionality only")
        print("   To enable OAuth: Set MUSICBRAINZ_CLIENT_ID and MUSICBRAINZ_CLIENT_SECRET")
    
    return True


async def main():
    """Main test function."""
    
    print("🎵 MusicBrainz API Test Suite")
    print("=" * 50)
    
    # Load environment variables if available
    try:
        from dotenv import load_dotenv
        if load_dotenv():
            print("✅ Loaded environment variables from .env file")
        else:
            print("ℹ️  No .env file found, using system environment variables")
    except ImportError:
        print("ℹ️  python-dotenv not installed, using system environment variables")
    
    print()
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above and try again.")
        return False
    
    print("\n" + "=" * 50)
    
    # Run tests
    success = await test_basic_functionality()
    
    if success:
        print("\n🎊 SUCCESS: MusicBrainz API client is ready to use!")
        return True
    else:
        print("\n💥 FAILED: Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
