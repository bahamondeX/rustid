use pyo3::prelude::*;
use pyo3::types::PyBytes;
use base64::{engine::general_purpose::{URL_SAFE_NO_PAD, STANDARD}, Engine as _};
use rayon::prelude::*;

#[pyclass]
#[derive(Clone, Copy)]
pub struct UUID {
    bytes: [u8; 16],
}

#[pymethods]
impl UUID {
    #[new]
    fn new(hex: Option<&str>, bytes: Option<Bound<'_, PyBytes>>) -> PyResult<Self> {
        if let Some(hex_str) = hex {
            let clean = hex_str.replace("-", "");
            if clean.len() != 32 {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid hex length"));
            }
            let mut bytes = [0u8; 16];
            for i in 0..16 {
                bytes[i] = u8::from_str_radix(&clean[i*2..i*2+2], 16)
                    .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid hex"))?;
            }
            Ok(UUID { bytes })
        } else if let Some(py_bytes) = bytes {
            let bytes_slice = py_bytes.as_bytes();
            if bytes_slice.len() != 16 {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid bytes length"));
            }
            let mut bytes = [0u8; 16];
            bytes.copy_from_slice(bytes_slice);
            Ok(UUID { bytes })
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Either hex or bytes required"))
        }
    }

    #[getter]
    fn hex(&self) -> String {
        hex::encode(self.bytes)
    }

    #[getter]
    fn bytes<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        PyBytes::new(py, &self.bytes)
    }

    #[getter]
    fn version(&self) -> u8 {
        (self.bytes[6] >> 4) & 0x0f
    }

    #[getter]
    fn variant(&self) -> String {
        let variant_bits = self.bytes[8] >> 6;
        match variant_bits {
            0b00 | 0b01 => "reserved for NCS compatibility".to_string(),
            0b10 => "specified in RFC 4122".to_string(),
            0b11 => "reserved for Microsoft compatibility".to_string(),
            _ => "unknown".to_string(),
        }
    }

    fn __str__(&self) -> String {
        format!("{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
            self.bytes[0], self.bytes[1], self.bytes[2], self.bytes[3],
            self.bytes[4], self.bytes[5], self.bytes[6], self.bytes[7],
            self.bytes[8], self.bytes[9], self.bytes[10], self.bytes[11],
            self.bytes[12], self.bytes[13], self.bytes[14], self.bytes[15])
    }

    fn __repr__(&self) -> String {
        format!("UUID('{}')", self.__str__())
    }

    fn __eq__(&self, other: &UUID) -> bool {
        self.bytes == other.bytes
    }

    fn __hash__(&self) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        let mut hasher = DefaultHasher::new();
        self.bytes.hash(&mut hasher);
        hasher.finish()
    }

    fn short_id(&self) -> String {
        URL_SAFE_NO_PAD.encode(&self.bytes[0..12])  // Use 12 bytes instead of 9
    }

    fn base64(&self) -> String {
        STANDARD.encode(&self.bytes)
    }

    fn int(&self) -> u128 {
        u128::from_be_bytes(self.bytes)
    }
}

#[pyfunction]
fn uuid1() -> UUID {
    let id = uuid::Uuid::now_v1(&[1, 2, 3, 4, 5, 6]);
    UUID { bytes: *id.as_bytes() }
}

#[pyfunction]
fn uuid4() -> UUID {
    let id = uuid::Uuid::new_v4();
    UUID { bytes: *id.as_bytes() }
}

#[pyfunction]
fn uuid7() -> UUID {
    let id = uuid::Uuid::now_v7();
    UUID { bytes: *id.as_bytes() }
}

#[pyfunction]
fn uuid4_batch(count: usize) -> Vec<UUID> {
    (0..count)
        .into_par_iter()
        .map(|_| UUID { bytes: *uuid::Uuid::new_v4().as_bytes() })
        .collect()
}

#[pyfunction]
fn uuid7_batch(count: usize) -> Vec<UUID> {
    (0..count)
        .into_par_iter()
        .map(|_| UUID { bytes: *uuid::Uuid::now_v7().as_bytes() })
        .collect()
}

#[pyfunction]
fn short_id() -> String {
    let id = uuid::Uuid::now_v7();
    URL_SAFE_NO_PAD.encode(&id.as_bytes()[0..12])  // Use 12 bytes for better uniqueness
}

#[pyfunction]
fn short_id_batch(count: usize) -> Vec<String> {
    (0..count)
        .into_par_iter()
        .map(|_| {
            let id = uuid::Uuid::now_v7();
            URL_SAFE_NO_PAD.encode(&id.as_bytes()[0..12])  // Use 12 bytes
        })
        .collect()
}

#[pyfunction]
#[pyo3(signature = (size=None))]
fn nano_id(size: Option<usize>) -> String {
    let alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_";
    let size = size.unwrap_or(21);
    let mut result = String::with_capacity(size);
    
    for _ in 0..size {
        let idx = fastrand::usize(0..alphabet.len());
        result.push(alphabet.chars().nth(idx).unwrap());
    }
    result
}

#[pyfunction]
#[pyo3(signature = (count, size=None))]
fn nano_id_batch(count: usize, size: Option<usize>) -> Vec<String> {
    let size = size.unwrap_or(21);
    (0..count)
        .into_par_iter()
        .map(|_| nano_id(Some(size)))
        .collect()
}

#[pymodule]
fn rustid(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<UUID>()?;
    m.add_function(wrap_pyfunction!(uuid1, m)?)?;
    m.add_function(wrap_pyfunction!(uuid4, m)?)?;
    m.add_function(wrap_pyfunction!(uuid7, m)?)?;
    m.add_function(wrap_pyfunction!(uuid4_batch, m)?)?;
    m.add_function(wrap_pyfunction!(uuid7_batch, m)?)?;
    m.add_function(wrap_pyfunction!(short_id, m)?)?;
    m.add_function(wrap_pyfunction!(short_id_batch, m)?)?;
    m.add_function(wrap_pyfunction!(nano_id, m)?)?;
    m.add_function(wrap_pyfunction!(nano_id_batch, m)?)?;
    Ok(())
}