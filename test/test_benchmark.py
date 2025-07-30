from rustid import generate_batch, generate_id
from uuid import uuid4
from time import perf_counter

def benchmark_rustid_individual():
	start_time = perf_counter()
	ids = [generate_id() for _ in range(1000000)]
	size = ids.__sizeof__()
	elapsed = perf_counter() - start_time
	print(f"RustID: {elapsed} seconds")
	assert elapsed > 0
	return {"elapsed": elapsed, "size": size}

def benchmark_rustid_batch():
	start_time = perf_counter()
	ids = generate_batch(1000000)
	size = ids.__sizeof__()
	elapsed = perf_counter() - start_time
	print(f"RustID: {elapsed} seconds")
	print(f"RustID: {size} bytes")
	assert elapsed > 0
	return {"elapsed": elapsed, "size": size}

def benchmark_uuid():
	start_time = perf_counter()
	ids = [uuid4() for _ in range(1000000)]
	size = ids.__sizeof__()
	elapsed = perf_counter() - start_time
	print(f"UUID: {elapsed} seconds")
	print(f"UUID: {size} bytes")
	assert elapsed > 0
	return {"elapsed": elapsed, "size": size}


def test_individual_elapsed():
	rustid_time = benchmark_rustid_individual()
	uuid_time = benchmark_uuid()
	print(f"RustID: {rustid_time['elapsed']} seconds")
	print(f"UUID: {uuid_time['elapsed']} seconds")
	assert rustid_time["elapsed"] <= uuid_time["elapsed"]

def test_batch_elapsed():
	rustid_time = benchmark_rustid_batch()
	uuid_time = benchmark_uuid()
	print(f"RustID: {rustid_time['elapsed']} seconds")
	print(f"UUID: {uuid_time['elapsed']} seconds")
	assert rustid_time["elapsed"] <= uuid_time["elapsed"]

def test_individual_size():
	rustid_time = benchmark_rustid_individual()
	uuid_time = benchmark_uuid()
	print(f"RustID: {rustid_time['size']} bytes")
	print(f"UUID: {uuid_time['size']} bytes")
	assert rustid_time["size"] <= uuid_time["size"]

def test_batch_size():
	rustid_time = benchmark_rustid_batch()
	uuid_time = benchmark_uuid()
	print(f"RustID: {rustid_time['size']} bytes")
	print(f"UUID: {uuid_time['size']} bytes")
	assert rustid_time["size"] <= uuid_time["size"]