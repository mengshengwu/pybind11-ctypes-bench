# pybind11 vs ctypes Performance Comparison

This project is designed to compare the performance difference between calling C functions from Python via pybind11 and ctypes. The test scenario focuses on passing strings in and returning strings from C functions.

## Project Structure

```
bench-py/
├── src/
│   ├── string_func.c          # C function implementation
│   ├── string_func.h          # C function header file
│   └── pybind11_module.cpp    # pybind11 wrapper module
├── benchmark.py               # Benchmark script
├── CMakeLists.txt             # CMake build configuration
└── README.md                  # Project documentation
```

## Build Requirements

- CMake 3.15 or newer
- C/C++ compiler (supporting C++11)
- Python 3.8 or newer
- pybind11 (included in the project)

## Build Steps

1. Create the build directory:
```bash
mkdir build
cd build
```

2. Run CMake configuration:
```bash
cmake ..
```

3. Build the project:
```bash
make
```

Alternatively, use CMake's build command:
```bash
cmake --build .
```

## Running the Benchmark

After building, run the benchmark from the project root:

```bash
python3 benchmark.py
```

Or run from the build directory (requires setting PYTHONPATH):

```bash
PYTHONPATH=build python3 benchmark.py
```

## Test Details

Performance testing includes the following scenarios:

1. **Short string**: about 13 characters
2. **Medium string**: 100 characters
3. **Long string**: 1000 characters
4. **Extra-long string**: 10,000 characters

Each test runs 100,000 iterations and collects:
- Average execution time (microseconds)
- Standard deviation
- Minimum/maximum execution time
- Performance comparison (pybind11 speed-up over ctypes)

## Implementation Details

### C Function

The `process_string()` function takes a string argument and returns a copied string. The caller is responsible for releasing the returned string's memory.

### pybind11 Implementation

Uses pybind11 to wrap the C function, automatically handling Python to C string conversion and memory management.

### ctypes Implementation

ctypes is used to directly call the compiled shared library. Manual handling is required for:
- String encoding/decoding (UTF-8)
- Memory management (by calling `free_string()` to release memory)

## Test Results

The following results were obtained on a Linux system (Arch Linux x86_64, WSL2) run on Ryzen 9 5950X CPU with 64GB RAM, running 100,000 iterations per test:

### Performance Summary

| Test Case | Length | pybind11 (μs) | ctypes (μs) | Speedup |
|-----------|--------|---------------|-------------|---------|
| Short string | 13 | 1.423 | 1.325 | 0.93x |
| Medium string | 100 | 1.480 | 1.336 | 0.90x |
| Long string | 1000 | 1.646 | 1.635 | 0.99x |
| Very long string | 10000 | 2.599 | 2.590 | 1.00x |

### Analysis

The test results show that for simple string operations:
- For short and medium strings, **ctypes is slightly faster** (about 7-10% faster)
- For long strings, the performance is **nearly identical** (within 1% difference)
- The performance difference is minimal (in the microsecond range) and may not be significant for most applications

**Key observations:**
1. Both methods have excellent performance, with execution times in the microsecond range
2. The performance gap decreases as string length increases
3. For simple string operations, the overhead difference between pybind11 and ctypes is negligible
4. The choice between pybind11 and ctypes should be based on development convenience, type safety, and project requirements rather than performance alone

## License

This project uses the same BSD license as pybind11.

