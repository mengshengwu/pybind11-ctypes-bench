#!/usr/bin/env python3
"""
Performance benchmark comparing pybind11 vs ctypes for string operations.
"""

import timeit
import statistics
import sys
import os
from pathlib import Path

# Add build directory to Python path to find the compiled module
build_dir = Path(__file__).parent / "build"
if build_dir.exists():
    sys.path.insert(0, str(build_dir))

# Try to import pybind11 module
try:
    import string_module
    PYBIND11_AVAILABLE = True
except ImportError as e:
    print(f"Warning: pybind11 module not found. Make sure to build it first.")
    print(f"  Import error: {e}")
    print(f"  Searched in: {build_dir}")
    PYBIND11_AVAILABLE = False

# Try to load ctypes library
try:
    import ctypes
    import platform
    
    # Determine library extension
    if platform.system() == "Windows":
        lib_ext = ".dll"
    elif platform.system() == "Darwin":
        lib_ext = ".dylib"
    else:
        lib_ext = ".so"
    
    # Try to find the shared library
    build_dir = Path(__file__).parent / "build"
    lib_paths = [
        build_dir / f"libstring_func{lib_ext}",
        build_dir / f"string_func{lib_ext}",
        Path(__file__).parent / f"libstring_func{lib_ext}",
        Path(__file__).parent / f"string_func{lib_ext}",
    ]
    
    lib_path = None
    for path in lib_paths:
        if path.exists():
            lib_path = path
            break
    
    if lib_path is None:
        # Try to find in current directory
        for path in Path(__file__).parent.glob(f"*string_func*{lib_ext}"):
            lib_path = path
            break
    
    if lib_path:
        lib = ctypes.CDLL(str(lib_path))
        lib.process_string.argtypes = [ctypes.c_char_p]
        lib.process_string.restype = ctypes.POINTER(ctypes.c_char)
        
        # Setup free_string function
        lib.free_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
        lib.free_string.restype = None
        
        def process_string_ctypes(input_str):
            """Wrapper for ctypes string processing."""
            if isinstance(input_str, str):
                input_bytes = input_str.encode('utf-8')
            else:
                input_bytes = input_str
            
            result_ptr = lib.process_string(input_bytes)
            if not result_ptr:
                return ""
            
            result = ctypes.string_at(result_ptr).decode('utf-8')
            # Free the memory allocated by C function
            lib.free_string(result_ptr)
            return result
        
        CTYPES_AVAILABLE = True
    else:
        print(f"Warning: ctypes library not found. Searched in: {lib_paths}")
        CTYPES_AVAILABLE = False
        process_string_ctypes = None
except Exception as e:
    print(f"Warning: Failed to load ctypes library: {e}")
    CTYPES_AVAILABLE = False
    process_string_ctypes = None


def benchmark_function(func, test_string, iterations=100000):
    """Benchmark a function with given test string and iterations."""
    times = []
    for _ in range(10):  # Run 10 times and take average
        start = timeit.default_timer()
        for _ in range(iterations):
            result = func(test_string)
        end = timeit.default_timer()
        times.append((end - start) / iterations)
    
    mean_time = statistics.mean(times)
    std_time = statistics.stdev(times) if len(times) > 1 else 0
    min_time = min(times)
    max_time = max(times)
    
    return {
        'mean': mean_time * 1e6,  # Convert to microseconds
        'std': std_time * 1e6,
        'min': min_time * 1e6,
        'max': max_time * 1e6,
        'total': sum(times) * 1e6,
    }


def run_benchmarks():
    """Run comprehensive benchmarks."""
    print("=" * 80)
    print("Performance Benchmark: pybind11 vs ctypes")
    print("=" * 80)
    print()
    
    # Test cases with different string lengths
    test_cases = [
        ("Short string", "Hello, World!"),
        ("Medium string", "A" * 100),
        ("Long string", "B" * 1000),
        ("Very long string", "C" * 10000),
    ]
    
    iterations = 100000
    
    results = []
    
    for test_name, test_string in test_cases:
        print(f"Testing: {test_name} (length: {len(test_string)})")
        print("-" * 80)
        
        result_row = {'test_name': test_name, 'string_length': len(test_string)}
        
        # Benchmark pybind11
        if PYBIND11_AVAILABLE:
            try:
                pybind11_stats = benchmark_function(
                    string_module.process_string,
                    test_string,
                    iterations
                )
                result_row['pybind11'] = pybind11_stats
                print(f"pybind11:")
                print(f"  Mean:   {pybind11_stats['mean']:.3f} μs")
                print(f"  Std:    {pybind11_stats['std']:.3f} μs")
                print(f"  Min:    {pybind11_stats['min']:.3f} μs")
                print(f"  Max:    {pybind11_stats['max']:.3f} μs")
            except Exception as e:
                print(f"pybind11: ERROR - {e}")
                result_row['pybind11'] = None
        else:
            print("pybind11: Not available")
            result_row['pybind11'] = None
        
        print()
        
        # Benchmark ctypes
        if CTYPES_AVAILABLE:
            try:
                ctypes_stats = benchmark_function(
                    process_string_ctypes,
                    test_string,
                    iterations
                )
                result_row['ctypes'] = ctypes_stats
                print(f"ctypes:")
                print(f"  Mean:   {ctypes_stats['mean']:.3f} μs")
                print(f"  Std:    {ctypes_stats['std']:.3f} μs")
                print(f"  Min:    {ctypes_stats['min']:.3f} μs")
                print(f"  Max:    {ctypes_stats['max']:.3f} μs")
            except Exception as e:
                print(f"ctypes: ERROR - {e}")
                result_row['ctypes'] = None
        else:
            print("ctypes: Not available")
            result_row['ctypes'] = None
        
        # Calculate speedup
        if result_row.get('pybind11') and result_row.get('ctypes'):
            speedup = result_row['ctypes']['mean'] / result_row['pybind11']['mean']
            print()
            print(f"Speedup: pybind11 is {speedup:.2f}x {'faster' if speedup > 1 else 'slower'} than ctypes")
        
        print()
        results.append(result_row)
    
    # Summary table
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"{'Test Case':<20} {'Length':<10} {'pybind11 (μs)':<15} {'ctypes (μs)':<15} {'Speedup':<10}")
    print("-" * 80)
    
    for row in results:
        test_name = row['test_name']
        length = row['string_length']
        pybind11_mean = f"{row['pybind11']['mean']:.3f}" if row.get('pybind11') else "N/A"
        ctypes_mean = f"{row['ctypes']['mean']:.3f}" if row.get('ctypes') else "N/A"
        
        if row.get('pybind11') and row.get('ctypes'):
            speedup = row['ctypes']['mean'] / row['pybind11']['mean']
            speedup_str = f"{speedup:.2f}x"
        else:
            speedup_str = "N/A"
        
        print(f"{test_name:<20} {length:<10} {pybind11_mean:<15} {ctypes_mean:<15} {speedup_str:<10}")
    
    print()


if __name__ == "__main__":
    if not PYBIND11_AVAILABLE and not CTYPES_AVAILABLE:
        print("Error: Neither pybind11 module nor ctypes library is available.")
        print("Please build the project first:")
        print("  mkdir build && cd build")
        print("  cmake ..")
        print("  make")
        sys.exit(1)
    
    run_benchmarks()

