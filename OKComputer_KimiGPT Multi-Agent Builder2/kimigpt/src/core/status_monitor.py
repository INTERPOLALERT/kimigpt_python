#!/usr/bin/env python3
"""
Real-time system status monitor for KimiGPT
Displays live status of all system components
"""

import time
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.api.api_manager import api_manager

def display_status():
    """Display current system status"""
    print("\033[2J\033[H", end='')  # Clear screen and move cursor to top
    
    print("🚀 KIMIGPT - REAL-TIME STATUS MONITOR")
    print("=" * 60)
    print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get API status
    status = api_manager.get_status()
    
    print("🔌 API PROVIDERS:")
    print("-" * 40)
    
    for api_name, api_info in status['apis'].items():
        status_icon = "✅" if api_info['status'] == 'online' else "❌"
        status_color = "\033[32m" if api_info['status'] == 'online' else "\033[31m"
        
        print(f"{status_icon} {api_name.upper():<15} {status_color}{api_info['status']:<12}\033[0m "
              f"({api_info['response_time']:.2f}s)")
    
    print()
    print("📊 SYSTEM METRICS:")
    print("-" * 40)
    print(f"   Active APIs: {status['online_apis']}/{status['total_apis']}")
    print(f"   Cache Entries: {status['cache_size']}")
    print(f"   System Health: {'✅ Healthy' if status['online_apis'] > 0 else '❌ Issues'}")
    
    print()
    print("💡 Press Ctrl+C to exit")

def main():
    """Main monitoring loop"""
    print("🚀 Starting KimiGPT Status Monitor...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            display_status()
            time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("\n\n👋 Status monitor stopped.")
        sys.exit(0)

if __name__ == '__main__':
    main()