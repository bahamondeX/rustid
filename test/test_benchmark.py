import time
import uuid
import rustid
import statistics
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def benchmark(func, iterations=100000, name=""):
    times = []
    for _ in range(5):  # 5 runs for statistical accuracy
        start = time.perf_counter()
        func(iterations)
        end = time.perf_counter()
        times.append(end - start)
    
    avg_time = statistics.mean(times)
    std_dev = statistics.stdev(times)
    ops_per_sec = iterations / avg_time
    
    print(f"{name:30} | {avg_time:8.4f}s ± {std_dev:6.4f} | {ops_per_sec:12,.0f} ops/s")
    return avg_time

def test_uuid4_single():
    def python_uuid4(n):
        for _ in range(n):
            uuid.uuid4()
    
    def rust_uuid4(n):
        for _ in range(n):
            rustid.uuid4()
    
    print("\n=== UUID4 Single Generation ===")
    py_time = benchmark(python_uuid4, 100000, "Python uuid4")
    rust_time = benchmark(rust_uuid4, 100000, "Rust uuid4")
    print(f"Speedup: {py_time/rust_time:.2f}x")

def test_uuid4_batch():
    def python_uuid4_batch(n):
        [uuid.uuid4() for _ in range(n)]
    
    def rust_uuid4_batch(n):
        rustid.uuid4_batch(n)
    
    print("\n=== UUID4 Batch Generation ===")
    py_time = benchmark(python_uuid4_batch, 100000, "Python uuid4 list comp")
    rust_time = benchmark(lambda n: rustid.uuid4_batch(n), 100000, "Rust uuid4_batch")
    print(f"Speedup: {py_time/rust_time:.2f}x")

def test_short_id():
    def python_short_id(n):
        import base64
        for _ in range(n):
            uid = uuid.uuid4()
            base64.urlsafe_b64encode(uid.bytes[:9]).decode().rstrip('=')
    
    def rust_short_id(n):
        for _ in range(n):
            rustid.short_id()
    
    def rust_short_id_batch(n):
        rustid.short_id_batch(n)
    
    print("\n=== Short ID Generation ===")
    py_time = benchmark(python_short_id, 50000, "Python short_id")
    rust_time = benchmark(rust_short_id, 50000, "Rust short_id")
    rust_batch_time = benchmark(lambda n: rustid.short_id_batch(n), 50000, "Rust short_id_batch")
    print(f"Single Speedup: {py_time/rust_time:.2f}x")
    print(f"Batch Speedup: {py_time/rust_batch_time:.2f}x")

def test_uuid_properties():
    def python_properties(n):
        for _ in range(n):
            uid = uuid.uuid4()
            str(uid)
            uid.hex
            uid.bytes
            uid.version
    
    def rust_properties(n):
        for _ in range(n):
            uid = rustid.uuid4()
            str(uid)
            uid.hex
            uid.bytes
            uid.version
    
    print("\n=== UUID Properties Access ===")
    py_time = benchmark(python_properties, 50000, "Python properties")
    rust_time = benchmark(rust_properties, 50000, "Rust properties")
    print(f"Speedup: {py_time/rust_time:.2f}x")

def test_massive_batch():
    sizes = [1000, 10000, 100000, 1000000]
    
    print("\n=== Massive Batch Generation ===")
    print("Size         | Python Time | Rust Time   | Speedup")
    print("-" * 55)
    
    for size in sizes:
        py_start = time.perf_counter()
        [uuid.uuid4() for _ in range(size)]
        py_time = time.perf_counter() - py_start
        
        rust_start = time.perf_counter()
        rustid.uuid4_batch(size)
        rust_time = time.perf_counter() - rust_start
        
        speedup = py_time / rust_time
        print(f"{size:8,} | {py_time:10.4f}s | {rust_time:10.4f}s | {speedup:6.2f}x")

def test_concurrent_generation():
    def python_concurrent(n):
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(lambda: [uuid.uuid4() for _ in range(n//4)]) for _ in range(4)]
            [f.result() for f in futures]
    
    def rust_concurrent(n):
        rustid.uuid4_batch(n)  # Already uses all cores
    
    print("\n=== Concurrent Generation ===")
    py_time = benchmark(python_concurrent, 100000, "Python concurrent (4 threads)")
    rust_time = benchmark(lambda n: rustid.uuid4_batch(n), 100000, "Rust parallel batch")
    print(f"Speedup: {py_time/rust_time:.2f}x")

def test_memory_usage():
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    print("\n=== Memory Usage Test ===")
    
    # Baseline
    baseline = process.memory_info().rss / 1024 / 1024
    
    # Python UUIDs
    start_mem = process.memory_info().rss / 1024 / 1024
    py_uuids = [uuid.uuid4() for _ in range(100000)]
    py_mem = process.memory_info().rss / 1024 / 1024
    del py_uuids
    
    # Rust UUIDs
    start_mem2 = process.memory_info().rss / 1024 / 1024
    rust_uuids = rustid.uuid4_batch(100000)
    rust_mem = process.memory_info().rss / 1024 / 1024
    del rust_uuids
    
    print(f"Baseline memory: {baseline:.1f} MB")
    print(f"Python UUIDs memory delta: {py_mem - start_mem:.1f} MB")
    print(f"Rust UUIDs memory delta: {rust_mem - start_mem2:.1f} MB")

def test_nano_id():
    def python_nano_id(n):
        import random
        import string
        alphabet = string.ascii_letters + string.digits + '-_'
        for _ in range(n):
            ''.join(random.choices(alphabet, k=21))
    
    def rust_nano_id(n):
        for _ in range(n):
            rustid.nano_id()
    
    def rust_nano_id_batch(n):
        rustid.nano_id_batch(n)
    
    print("\n=== NanoID Generation ===")
    py_time = benchmark(python_nano_id, 50000, "Python nano_id")
    rust_time = benchmark(rust_nano_id, 50000, "Rust nano_id")
    rust_batch_time = benchmark(lambda n: rustid.nano_id_batch(n), 50000, "Rust nano_id_batch")
    print(f"Single Speedup: {py_time/rust_time:.2f}x")
    print(f"Batch Speedup: {py_time/rust_batch_time:.2f}x")

def test_correctness():
    print("\n=== Correctness Tests ===")
    
    # Test UUID4 uniqueness
    rust_uuids = set(str(rustid.uuid4()) for _ in range(10000))
    py_uuids = set(str(uuid.uuid4()) for _ in range(10000))
    
    print(f"Rust UUID4 uniqueness: {len(rust_uuids)} / 10000")
    print(f"Python UUID4 uniqueness: {len(py_uuids)} / 10000")
    
    # Test UUID format
    rust_uuid = rustid.uuid4()
    py_uuid = uuid.uuid4()
    
    print(f"Rust UUID format: {rust_uuid}")
    print(f"Python UUID format: {py_uuid}")
    print(f"Rust UUID version: {rust_uuid.version}")
    print(f"Python UUID version: {py_uuid.version}")
    
    # Test short ID uniqueness
    short_ids = set(rustid.short_id_batch(10000))
    print(f"Short ID uniqueness: {len(short_ids)} / 10000")
    print(f"Short ID example: {rustid.short_id()}")
    
    # Test batch equality
    batch1 = rustid.uuid4_batch(1000)
    batch2 = rustid.uuid4_batch(1000)
    overlaps = len(set(str(u) for u in batch1) & set(str(u) for u in batch2))
    print(f"Batch overlap (should be 0): {overlaps}")

if __name__ == "__main__":
    print("🚀 UUID Performance Benchmark")
    print("=" * 60)
    
    test_correctness()
    test_uuid4_single()
    test_uuid4_batch()
    test_short_id()
    test_uuid_properties()
    test_nano_id()
    test_massive_batch()
    test_concurrent_generation()
    test_memory_usage()
    
    print("\n" + "=" * 60)
    print("✅ Benchmark complete!")