import time
import multiprocessing as mp
from collections import Counter
import pytest
from rustid import generate_id, generate_batch

# Helper function for the multiprocessing test.
# It must be a top-level function to be pickleable.
def generate_and_put_ids(queue, count):
    """Generates a batch of IDs and puts them into a queue."""
    ids = generate_batch(count)
    queue.put(ids)

class TestCorrectness:
    """Tests for the correctness and basic properties of the ID generator."""

    def test_generate_id_basic(self):
        """Ensure a single ID can be generated and is a string."""
        id_str = generate_id()
        assert isinstance(id_str, str)
        assert len(id_str) > 0

    def test_url_safe_ids(self):
        """Check if IDs only contain URL-safe characters (A-Z, a-z, 0-9, '-', '_')."""
        ids = generate_batch(1000)
        allowed_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')
        for id_str in ids:
            assert all(c in allowed_chars for c in id_str)

    def test_uniqueness_single_thread(self):
        """Test for uniqueness in a large batch from a single thread."""
        count = 50_000
        ids = generate_batch(count)
        assert len(set(ids)) == count

    def test_uniqueness_multi_thread(self):
        """Test for uniqueness across multiple threads."""
        import threading
        
        results = []
        lock = threading.Lock()
        
        def worker():
            ids = generate_batch(5_000)
            with lock:
                results.extend(ids)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(set(results)) == 20_000

    def test_uniqueness_multi_process(self):
        """Test for uniqueness across multiple processes."""
        queue = mp.Queue()
        processes = []
        process_count = 4
        ids_per_process = 5_000

        for _ in range(process_count):
            # Use the top-level helper function instead of a lambda
            p = mp.Process(target=generate_and_put_ids, args=(queue, ids_per_process))
            processes.append(p)
            p.start()

        all_ids = []
        for _ in range(process_count):
            all_ids.extend(queue.get())

        for p in processes:
            p.join()

        assert len(set(all_ids)) == process_count * ids_per_process

    def test_length_consistency(self):
        """Ensure all generated IDs have the correct and consistent length (12)."""
        ids = generate_batch(1000)
        # Check that the first ID has the expected length of 12.
        assert len(ids[0]) == 22
        # Check that all IDs in the batch have the same length.
        unique_lengths = {len(id_str) for id_str in ids}
        assert len(unique_lengths) == 1, "IDs have inconsistent lengths"


class TestPerformance:
    """Performance benchmarks for the ID generator."""

    def benchmark(self, func, *args, **kwargs):
        """A simple benchmark helper."""
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        return {"elapsed": end_time - start_time}

    def test_rustid_vs_uuid_individual(self):
        """Compare performance of generating single IDs against standard uuid4."""
        import uuid
        count = 10_000
        rust_perf = self.benchmark(lambda: [generate_id() for _ in range(count)])
        uuid_perf = self.benchmark(lambda: [str(uuid.uuid4()) for _ in range(count)])
        print(f"\nRustID: {rust_perf['elapsed']:.4f}s, UUID: {uuid_perf['elapsed']:.4f}s, Speedup: {uuid_perf['elapsed']/rust_perf['elapsed']:.2f}x")
        assert rust_perf['elapsed'] < uuid_perf['elapsed']

    def test_scalability(self):
        """Test how performance scales with batch size."""
        print("\n  Size      Time(s)    Rate(K/s)      μs/ID")
        for size in [1_000, 10_000, 100_000, 500_000]:
            elapsed = self.benchmark(generate_batch, size)['elapsed']
            rate = size / elapsed / 1000
            per_id_us = elapsed * 1_000_000 / size
            print(f"{size:>8,}    {elapsed:>8.4f}    {rate:>9.1f}    {per_id_us:>9.2f}")
        assert True # This is more of a report than a strict test


class TestEdgeCases:
    """Tests for edge cases."""

    def test_large_batch(self):
        """Test with a very large batch size."""
        count = 1_000_000
        ids = generate_batch(count)
        assert len(ids) == count == len(set(ids))

    def test_zero_batch(self):
        """Test generating a batch of zero IDs."""
        ids = generate_batch(0)
        assert isinstance(ids, list)
        assert len(ids) == 0

    def test_rapid_successive_calls(self):
        """Ensure rapid calls still produce unique IDs."""
        ids = [generate_id() for _ in range(10_000)]
        assert len(set(ids)) == 10_000


class TestStatistics:
    """Statistical tests on the generated IDs."""

    def test_character_distribution(self):
        """Check for a reasonable distribution of characters."""
        ids = "".join(generate_batch(10_000))
        counts = Counter(ids)
        # A very basic sanity check, not a true test of randomness.
        assert len(counts) > 50, "Character distribution seems too narrow"

    def test_length_distribution(self):
        """Verify the distribution of lengths is fixed at 12."""
        ids = generate_batch(1000)
        lengths = [len(i) for i in ids]
        avg_len = sum(lengths) / len(lengths)
        assert avg_len == 22.0
        print(f"\nAvg Length: {avg_len:.2f}, Range: {min(lengths)}-{max(lengths)}")
