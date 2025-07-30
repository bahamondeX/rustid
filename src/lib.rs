// src/lib.rs: The core logic for the unique ID generator.

use pyo3::prelude::*;
use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
use rayon::prelude::*; // For parallel processing

/// # Internal function to generate a single URL-safe ID.
///
/// It creates a time-ordered UUID v7 and truncates it to 9 bytes,
/// which are then Base64 encoded into a 12-character string.
///
/// WARNING: Truncating the ID to 12 characters (from 72 bits of data) significantly
/// increases the probability of collisions compared to using the full 
/// 22-character (128-bit) UUID. For applications requiring extremely high
/// uniqueness guarantees (e.g., billions of IDs generated per second),
/// consider using the full 128-bit UUID or a different ID generation strategy.
#[inline]
fn generate_one_id() -> String {
    // 1. Generate a new UUID version 7 (128 bits / 16 bytes).
    //    `now_v7()` is highly optimized and uses a timestamp with millisecond precision,
    //    plus random bits to ensure uniqueness.
    let id = uuid::Uuid::now_v7();
    let full_id_bytes = id.as_bytes();

    // 2. Truncate to the first 9 bytes (72 bits).
    //    This preserves the time-based sorting property of UUIDv7 while
    //    reducing the length. The first 6 bytes contain the timestamp.
    let truncated_bytes = &full_id_bytes[0..9];

    // 3. Encode the 9 bytes into a 12-character URL-safe Base64 string.
    //    URL_SAFE_NO_PAD ensures characters like '+' and '/' are replaced
    //    and no padding '=' characters are added.
    URL_SAFE_NO_PAD.encode(truncated_bytes)
}

/// Generates a single, 12-character, URL-safe, time-sortable unique ID.
///
/// This ID is based on a truncated UUID v7, ensuring it is time-ordered
/// and suitable for use in URLs or filenames.
///
/// WARNING: The shorter 12-character length increases the probability of
/// collisions compared to longer, full UUIDs. Use with caution for
/// extremely high-volume ID generation scenarios where collision
/// probability must be minimized.
///
/// Returns:
///     str: A 12-character URL-safe unique ID string.
#[pyfunction]
fn generate_id() -> String {
    generate_one_id()
}

/// Generates a batch of unique IDs in parallel for maximum performance.
///
/// This function leverages the `rayon` crate to parallelize the ID generation
/// process across all available CPU cores, making it extremely fast for large batches.
/// Each ID generated is a 12-character, URL-safe, time-sortable unique ID.
///
/// Args:
///     count (int): The number of unique IDs to generate.
///
/// Returns:
///     list[str]: A list containing the generated 12-character unique IDs.
#[pyfunction]
fn generate_batch(count: usize) -> Vec<String> {
    // Use a parallel iterator provided by `rayon` to generate the IDs.
    // `(0..count).into_par_iter()` creates a parallel iterator that will
    // distribute the work of calling `generate_one_id()` across multiple threads.
    (0..count)
        .into_par_iter()
        .map(|_| generate_one_id())
        .collect()
}

/// # The Python module definition.
///
/// This block uses the `#[pymodule]` macro from PyO3 to define the Python module.
/// The module is named `rustid`, matching the `[lib]` name specified in `Cargo.toml`.
///
/// Functions exposed to Python must be added to the module using `m.add_function()`.
///
/// Args:
///     _py (Python): The Python interpreter instance (often not directly used
///                   when only adding functions).
///     m (Bound<'_, PyModule>): A mutable reference to the Python module object.
///
/// Returns:
///     PyResult<()>: A result indicating success or failure.
#[pymodule]
fn rustid(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add the Rust functions `generate_id` and `generate_batch` to the Python module.
    // `wrap_pyfunction!` is a macro that converts a Rust function into a Python callable.
    m.add_function(wrap_pyfunction!(generate_id, m)?)?;
    m.add_function(wrap_pyfunction!(generate_batch, m)?)?;
    Ok(())
}