#!/usr/bin/env python3
"""
API testing script for KimiGPT
Tests all configured APIs and reports their status
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.api.api_manager import api_manager

async def test_all_apis():
    """Test all configured APIs"""
    print("🚀 Starting API Tests...")
    print("=" * 50)
    
    # Get current API status
    status = api_manager.get_status()
    
    print(f"📊 System Overview:")
    print(f"   Total APIs: {status['total_apis']}")
    print(f"   Online APIs: {status['online_apis']}")
    print(f"   Cache Size: {status['cache_size']} entries")
    print()
    
    # Test each API
    for api_name, api_status in status['apis'].items():
        print(f"🔌 {api_name.upper()} API:")
        print(f"   Status: {api_status['status']}")
        print(f"   Response Time: {api_status['response_time']:.3f}s")
        print(f"   Success Rate: {api_status['success_rate']:.2%}")
        print(f"   Error Count: {api_status['error_count']}")
        print(f"   Last Used: {api_status['last_used']}")
        
        if api_status['status'] == 'online':
            print("   ✅ API is working correctly")
        elif api_status['status'] == 'rate_limited':
            print("   ⚠️  API is rate limited")
        else:
            print("   ❌ API is offline")
        print()
    
    # Overall assessment
    online_count = sum(1 for api in status['apis'].values() if api['status'] == 'online')
    total_count = len(status['apis'])
    
    print("📈 Overall Assessment:")
    if online_count == total_count:
        print("   🎉 All APIs are online and working!")
        print("   ✅ System is ready for website generation")
    elif online_count > 0:
        print(f"   ⚠️  {online_count}/{total_count} APIs are online")
        print("   ✅ System can still function with available APIs")
    else:
        print("   ❌ No APIs are currently available")
        print("   🔧 Please check your API configurations")
    
    return online_count > 0

async def main():
    """Main testing function"""
    try:
        success = await test_all_apis()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error during API testing: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())