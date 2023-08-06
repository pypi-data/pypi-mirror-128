#include <pybind11/pybind11.h>
#include "trades.h"

namespace py = pybind11;

PYBIND11_MODULE(trades, m) {
    py::class_<Trades>(m, "Trades")
        .def(py::init<std::string>())
        .def("add", &Trades::add)
        .def_readonly("len", &Trades::len);
}
