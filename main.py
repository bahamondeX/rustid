#!/usr/bin/env python3
import time
import uuid
import rustid

def quick_test():
    print("Testing basic functionality...")
    
    # Test single generation
    rust_uuid = rustid.uuid4()
    py_uuid = uuid.uuid4()
    
    print(f"Rust UUID: {rust_uuid}")
    print(f"Python UUID: {py_uuid}")
    print(f"Short ID: {rustid.short_id()}")
    print(f"NanoID: {rustid.nano_id()}")
    
    # Quick speed test
    n = 10000
    
    start = time.time()
    [uuid.uuid4() for _ in range(n)]
    py_time = time.time() - start
    
    start = time.time()
    rustid.uuid4_batch(n)
    rust_time = time.time() - start
    
    print(f"\nSpeed test ({n:,} UUIDs):")
    print(f"Python: {py_time:.4f}s ({n/py_time:,.0f} ops/s)")
    print(f"Rust: {rust_time:.4f}s ({n/rust_time:,.0f} ops/s)")
    print(f"Speedup: {py_time/rust_time:.1f}x")

if __name__ == "__main__":
    quick_test()