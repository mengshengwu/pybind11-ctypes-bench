#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include "string_func.h"

namespace py = pybind11;

std::string process_string_pybind11(const std::string& input) {
    char* result = process_string(input.c_str());
    if (result == NULL) {
        return std::string();
    }
    std::string output(result);
    free_string(result);
    return output;
}

PYBIND11_MODULE(string_module, m) {
    m.doc() = "String processing module using pybind11";
    
    m.def("process_string", &process_string_pybind11,
          "Process a string and return the result",
          py::arg("input"));
}

