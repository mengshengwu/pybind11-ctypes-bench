cmake_minimum_required(VERSION 3.15)

project(bench_py C CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add pybind11 subdirectory
add_subdirectory(pybind11)

# Build shared library for ctypes
add_library(string_func_shared SHARED
    src/string_func.c
    src/string_func.h
)

# Set output name for shared library
if(UNIX AND NOT APPLE)
    set_target_properties(string_func_shared PROPERTIES
        OUTPUT_NAME "string_func"
        PREFIX "lib"
    )
elseif(APPLE)
    set_target_properties(string_func_shared PROPERTIES
        OUTPUT_NAME "string_func"
        PREFIX "lib"
    )
elseif(WIN32)
    set_target_properties(string_func_shared PROPERTIES
        OUTPUT_NAME "string_func"
    )
endif()

# Build pybind11 module
pybind11_add_module(string_module
    src/pybind11_module.cpp
    src/string_func.c
)

# Set output directory for both targets
set_target_properties(string_func_shared string_module PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
)

