"""Test password to see what's being passed"""
import sys

# Simulate the password that might be sent
test_password = sys.argv[1] if len(sys.argv) > 1 else "testpass10"

print(f"Password: {test_password}")
print(f"Length: {len(test_password)}")
print(f"Length in bytes: {len(test_password.encode('utf-8'))}")
print(f"First 20 chars: {test_password[:20]}")

# Try to hash it
from src.utils.security import hash_password

try:
    hashed = hash_password(test_password)
    print(f"✓ Hashing succeeded")
    print(f"Hash: {hashed[:30]}...")
except Exception as e:
    print(f"✗ Hashing failed: {e}")
