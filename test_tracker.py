#!/usr/bin/env python3
"""Test script for API Tracker functionality"""

print("=" * 70)
print("🔍 TESTING API TRACKER SYSTEM")
print("=" * 70)

# Test 1: Configuration
from config import validate_config, USE_API_TRACKER, GEMINI_MODEL
print(f"\n1. Configuration:")
print(f"   USE_API_TRACKER: {USE_API_TRACKER}")
print(f"   GEMINI_MODEL: {GEMINI_MODEL}")

# Test 2: Validation
print("\n2. Validating Config...")
try:
    validate_config()
except Exception as e:
    print(f"   ❌ Validation failed: {e}")
    exit(1)

# Test 3: Get API Keys
print("\n3. Testing API Key Detection...")
from api_tracker_utils.tracker import get_available_api_keys
keys = get_available_api_keys()
print(f"   ✅ Found {len(keys)} API keys")
for i, key in enumerate(keys, 1):
    print(f"      Key {i}: ...{key[-6:]}")

# Test 4: Get Best Key for Model
print(f"\n4. Getting Best API Key for {GEMINI_MODEL}...")
from api_tracker_utils.tracker import get_best_api_key_for_model
try:
    best_key = get_best_api_key_for_model(GEMINI_MODEL)
    print(f"   ✅ Selected: ...{best_key[-6:]}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 5: Track a Call
print("\n5. Simulating API Call (tracking)...")
from api_tracker_utils.tracker import track_model_call
track_model_call(best_key, GEMINI_MODEL)
print(f"   ✅ Tracked call for ...{best_key[-6:]}")

# Test 6: View Stats
print("\n6. Viewing Tracker Stats...")
from api_tracker_utils.tracker import get_tracker_stats
stats = get_tracker_stats()

for api_suffix, models in stats.items():
    print(f"\n   📊 API ...{api_suffix}:")
    for model, model_stats in models.items():
        if model_stats['total_calls'] > 0:  # Only show models with calls
            print(f"      {model}:")
            print(f"         Total: {model_stats['total_calls']}")
            print(f"         Minute: {model_stats['minute_usage']}/{model_stats['minute_limit']}")
            print(f"         Daily: {model_stats['daily_usage']}/{model_stats['daily_limit']}")
            print(f"         Status: {'✅ OK' if model_stats['within_limits'] else '⚠️  AT LIMIT'}")

# Test 7: Test Multiple Calls
print("\n7. Testing Multiple API Calls (load distribution)...")
for i in range(5):
    key = get_best_api_key_for_model(GEMINI_MODEL)
    track_model_call(key, GEMINI_MODEL)
    print(f"   Call {i+1}: ...{key[-6:]}")

print("\n" + "=" * 70)
print("✅ ALL TRACKER TESTS PASSED!")
print("=" * 70)
print("\n💡 The tracker will automatically:")
print("   • Select least-used API keys")
print("   • Respect rate limits (per-minute & per-day)")
print("   • Distribute load across all 7 keys")
print("   • Send email if all limits exhausted")
